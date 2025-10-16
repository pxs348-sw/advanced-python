import time
import asyncio

async def brewCoffee():
    print("Start brewCoffee()")
    await asyncio.sleep(3)
    print("End brewCoffee()")
    return "Coffee ready"

async def toastBagel():
    print("Start toastBagel()")
    await asyncio.sleep(2)
    print("End toastBagel()")
    return "Bagel toasted"

async def main():
    start_time = time.time()

    batch = asyncio.gather(brewCoffee(), toastBagel())
    result_coffee, result_bagel = await batch

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"result of brewCoffee: {result_coffee}")
    print(f"result of toastBagel: {result_bagel}")
    print(f"total execution time: {elapsed_time}")

if __name__ == "__main__":
    asyncio.run(main())