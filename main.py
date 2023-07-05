from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")


def introduce_yourself():
    robot.say_hello()


def retrieve_information_on_scientists():
    robot.retrieve_information_on_scientists(SCIENTISTS)


def additional_statistics():
    robot.generate_additional_statistics()
    robot.print_additional_statistics()


def goodbye():
    robot.say_goodbye()


def main():
    introduce_yourself()
    retrieve_information_on_scientists()
    additional_statistics()
    goodbye()


if __name__ == "__main__":
    main()
