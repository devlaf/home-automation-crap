#!/usr/bin/env python3

import anki_vector

def test(args):
    with anki_vector.Robot(args.serial) as robot:
        print("Say 'Hello World'...")
        robot.say_text("Hello World")


def main():
    args = anki_vector.util.parse_command_args()
    test(args)

if __name__ == "__main__":
    main()
