from SQLManagement import MovieSQLCreation, ShowSQLCreation


def main():
    while True:
        action = input("Which type of information do you want to interact with:\n"
                       "movies\n"
                       "shows\n"
                       "quit\n")

        if action == "movies":
            MovieSQLCreation.main()
        elif action == "shows":
            ShowSQLCreation.main()
        elif action == "quit":
            exit(0)
        else:
            print("Please enter a valid input.\n")


if __name__ == "__main__":
    main()
