---
title: _dl_runtime_resolve
created: 2022-09-08 16:48:16
updated: 2022-09-11 02:00:14
tags: 
- atom
---
# _dl_runtime_resolve

1. 首先用`link_map`访问`.dynamic`，分别取出`.dynstr`、`.dynsym`、`.rel.plt`的地址
2. `.rel.plt`+参数`relic_index`，求出当前函数的重定位表项`Elf32_Rel`的指针，记作`rel`
3. `rel->r_info` >> `8` 作为`.dynsym`的下标，求出当前函数的符号表项`Elf32_Sym`的指针，记作`sym`
4. `.dynstr` + `sym->st_name`得出符号名 字符串指针
5. 在动态链接库查找这个函数的地址，并且把地址赋值给`*rel->r_offset`，即`GOT`表
6. 最后调用这个函数

![[z-oblib/z2-attachments/Pasted image 20220911014856.png]]

## 方法过程

[6.1.3 pwn XDCTF2015 pwn200 · CTF All In One (gitbooks.io)](https://firmianay.gitbooks.io/ctf-all-in-one/content/doc/6.1.3_pwn_xdctf2015_pwn200.html)

```asm
gdb-peda$ disassemble 0xf7fec370
Dump of assembler code for function _dl_runtime_resolve:
   0xf7fec370 <+0>:     push   eax
   0xf7fec371 <+1>:     push   ecx
   0xf7fec372 <+2>:     push   edx
   0xf7fec373 <+3>:     mov    edx,DWORD PTR [esp+0x10]
   0xf7fec377 <+7>:     mov    eax,DWORD PTR [esp+0xc]
   0xf7fec37b <+11>:    call   0xf7fe6080 <_dl_fixup>
   0xf7fec380 <+16>:    pop    edx
   0xf7fec381 <+17>:    mov    ecx,DWORD PTR [esp]
   0xf7fec384 <+20>:    mov    DWORD PTR [esp],eax
   0xf7fec387 <+23>:    mov    eax,DWORD PTR [esp+0x4]
   0xf7fec38b <+27>:    ret    0xc
End of assembler dump.
```

该函数在 `glibc/sysdeps/i386/dl-trampoline.S` 中用汇编实现，先保存寄存器，然后将两个值分别传入寄存器，调用 `_dl_fixup`，最后恢复寄存器。
这里传递的参数就是动态链接时压入的两个参数：

```asm
gdb-peda$ x/w $esp+0x10
0xffffd598:     0x00000020
gdb-peda$ x/w $esp+0xc
0xffffd594:     0xf7ffd900
```

一个是在 `<write@plt+6>: push 0x20` 中压入的偏移量，一个是 PLT[0] 中 `push DWORD PTR ds:0x804a004` 压入的 GOT[1]。

函数 `_dl_fixup(struct link_map *l, ElfW(Word) reloc_arg)`，其参数分别由寄存器 `eax` 和 `edx` 提供。
即使我们使用单步进入，也不能调试 `_dl_fixup`，它直接就执行完成并跳转到 write 函数了，而此时，GOT 的地址已经被覆盖为实际地址：

```
gdb-peda$ x/w 0x804a01c
0x804a01c:      0xf7ea3100
```

再强调一遍：fixup 是通过寄存器取参数的，这似乎违背了 32 位程序的调用约定，但它就是这样，上面 gdb 中显示的参数是错误的，该函数对程序员来说是透明的，所以会尽量少用栈去做操作。

既然不能调试，直接看代码吧，在 `glibc/elf/dl-runtime.c` 中：

```c
DL_FIXUP_VALUE_TYPE
attribute_hidden __attribute ((noinline)) ARCH_FIXUP_ATTRIBUTE
_dl_fixup (
# ifdef ELF_MACHINE_RUNTIME_FIXUP_ARGS
       ELF_MACHINE_RUNTIME_FIXUP_ARGS,
# endif
       struct link_map *l, ElfW(Word) reloc_arg)
{
  // 分别获取动态链接符号表和动态链接字符串表的基址
  const ElfW(Sym) *const symtab
    = (const void *) D_PTR (l, l_info[DT_SYMTAB]);
  const char *strtab = (const void *) D_PTR (l, l_info[DT_STRTAB]);

  // 通过参数 reloc_arg 计算重定位入口，这里的 DT_JMPREL 即 .rel.plt，reloc_offset 即 reloc_arg
  const PLTREL *const reloc
    = (const void *) (D_PTR (l, l_info[DT_JMPREL]) + reloc_offset);

  // 根据函数重定位表中的动态链接符号表索引，即 reloc->r_info，获取函数在动态链接符号表中对应的条目
  const ElfW(Sym) *sym = &symtab[ELFW(R_SYM) (reloc->r_info)];
  const ElfW(Sym) *refsym = sym;
  void *const rel_addr = (void *)(l->l_addr + reloc->r_offset);
  lookup_t result;
  DL_FIXUP_VALUE_TYPE value;

  /* Sanity check that we're really looking at a PLT relocation.  */
  assert (ELFW(R_TYPE)(reloc->r_info) == ELF_MACHINE_JMP_SLOT);

   /* Look up the target symbol.  If the normal lookup rules are not
      used don't look in the global scope.  */
  if (__builtin_expect (ELFW(ST_VISIBILITY) (sym->st_other), 0) == 0)
    {
      const struct r_found_version *version = NULL;

      if (l->l_info[VERSYMIDX (DT_VERSYM)] != NULL)
    {
      const ElfW(Half) *vernum =
        (const void *) D_PTR (l, l_info[VERSYMIDX (DT_VERSYM)]);
      ElfW(Half) ndx = vernum[ELFW(R_SYM) (reloc->r_info)] & 0x7fff;
      version = &l->l_versions[ndx];
      if (version->hash == 0)
        version = NULL;
    }

      /* We need to keep the scope around so do some locking.  This is
     not necessary for objects which cannot be unloaded or when
     we are not using any threads (yet).  */
      int flags = DL_LOOKUP_ADD_DEPENDENCY;
      if (!RTLD_SINGLE_THREAD_P)
    {
      THREAD_GSCOPE_SET_FLAG ();
      flags |= DL_LOOKUP_GSCOPE_LOCK;
    }

#ifdef RTLD_ENABLE_FOREIGN_CALL
      RTLD_ENABLE_FOREIGN_CALL;
#endif
      // 根据 strtab+sym->st_name 在字符串表中找到函数名，然后进行符号查找获取 libc 基址 result
      result = _dl_lookup_symbol_x (strtab + sym->st_name, l, &sym, l->l_scope,
                    version, ELF_RTYPE_CLASS_PLT, flags, NULL);

      /* We are done with the global scope.  */
      if (!RTLD_SINGLE_THREAD_P)
    THREAD_GSCOPE_RESET_FLAG ();

#ifdef RTLD_FINALIZE_FOREIGN_CALL
      RTLD_FINALIZE_FOREIGN_CALL;
#endif

      /* Currently result contains the base load address (or link map)
     of the object that defines sym.  Now add in the symbol
   offset.  */

      // 将要解析的函数的偏移地址加上 libc 基址，得到函数的实际地址
      value = DL_FIXUP_MAKE_VALUE (result,
                   sym ? (LOOKUP_VALUE_ADDRESS (result)
                      + sym->st_value) : 0);
    }
  else
    {
      /* We already found the symbol.  The module (and therefore its load
     address) is also known.  */
      value = DL_FIXUP_MAKE_VALUE (l, l->l_addr + sym->st_value);
      result = l;
    }

  /* And now perhaps the relocation addend.  */
  value = elf_machine_plt_value (l, reloc, value);

  // 将已经解析完成的函数地址写入相应的 GOT 表中
  if (sym != NULL
      && __builtin_expect (ELFW(ST_TYPE) (sym->st_info) == STT_GNU_IFUNC, 0))
    value = elf_ifunc_invoke (DL_FIXUP_VALUE_ADDR (value));

  /* Finally, fix up the plt itself.  */
  if (__glibc_unlikely (GLRO(dl_bind_not)))
    return value;

  return elf_machine_fixup_plt (l, result, refsym, sym, reloc, rel_addr, value);
}
```