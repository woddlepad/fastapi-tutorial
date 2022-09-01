import uvicorn


def main():
    uvicorn.run("first_api.api.run:app", reload=True, host="localhost", port=8000)


if __name__ == "__main__":
    main()
