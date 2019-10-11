import asyncio
import sys
import select
#import test1

@asyncio.coroutine
def main():
    while True:
        mode = input("Enter mode: ")
        print(mode)
        type(mode)
        if mode == '1':
            print("Here I do stuff")
            #test1.do_stuff()
        else:
            print("I don't know what to do")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
