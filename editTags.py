import os

if __name__ == '__main__':
    for root, dirs, files in os.walk("."):
        for filename in files:
            if filename.split('.')[-1] != 'md':
                continue
            print(filename)
            all_name = os.path.join(root, filename)
            print(all_name)
            with open(all_name, 'r+', encoding='utf-8') as f:
                d = f.read()
                t = d.replace('#atom', 'atom')
                f.seek(0, 0)
                f.write(t)