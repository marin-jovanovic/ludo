

def get_last(portfolio):
    t = requests.get(
        f"{url}/{portfolio}",
        data={
            "options": "last"
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))


def patch():

    t = requests.patch(
        url + "d",
        data={
            "name": "d",
            "colour": "p"

        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))

def delete(portfolio):
    print(f"{portfolio=}")
    t = requests.delete(
        f"{url}/{portfolio}",
        data={
            # "portfolio": portfolio
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))

def main():
    # for i in range(15):
    #     post(portfolio="portfolio_1", colour=str(i))
    # delete("portfolio_1")
    # get_all("portfolio_1")
    get_last("portfolio_1")

if __name__ == '__main__':
    main()