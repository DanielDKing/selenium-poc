from ryanair_api import RyanairAPI


def main():
    api = RyanairAPI()
    api.gather_data()


if __name__ == "__main__":
    main()
