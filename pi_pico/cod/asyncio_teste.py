import uasyncio as asyncio

async def minha_funcao():
    while True:
        print("Função rodando...")
        await asyncio.sleep(1)  # Pause por 1 segundo

async def loop_principal():
    while True:
        print("Loop principal rodando...")
        await asyncio.sleep(0.5)  # Pause por 0.5 segundo

async def main():
    # Executa as duas funções em paralelo
    await asyncio.gather(
        minha_funcao(),
        loop_principal(),
    )

# Inicia o event loop
asyncio.run(main())