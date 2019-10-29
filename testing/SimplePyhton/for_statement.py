class C:
    def __iter__(self):
        return iter(range(3))


def main():
    c = C()
    for i in c:
        print(i)
    else:
        print('StopIteration')


if __name__ == "__main__":
    main()
