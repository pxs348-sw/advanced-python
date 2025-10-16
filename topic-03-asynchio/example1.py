import time

def brewCoffee():
    print("Start brewCoffee()")
    time.sleep(3)
    print("End brewCoffee()")
    return "Coffee ready"

def toastBagel():
    print("Start toastBagel()")
    time.sleep(2)
    print("End toastBagel()")
    return "Bagel toasted"

def main():
    start_time = time.time()

    result_coffee = brewCoffee()
    result_bagel = toastBagel()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"result of brewCoffee: {result_coffee}")
    print(f"result of toastBagel: {result_bagel}")
    print(f"total execution time: {elapsed_time}")

if __name__ == "__main__":
    main()