import sys


def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing "
              "<config.txt>")
        sys.exit()
    AMazeIng()


if __name__ == "__main__":
    main()
