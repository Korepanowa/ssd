from zeep import Client

print("Выбор категории:")
print("1: CountryInfoService")
print("2: NumberConversion")

choice = input("Введите цифру:")

url1 = 'https://www.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
url2 = 'https://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL'

if choice == "1":
    print(f"Доступные методы:")
    client = Client(url1)                                                                 
    methods = [method for method in dir(client.service) if not method.startswith('__')]

    for method in methods:
        print(f"+ {method}")

    method = input("Введите выбранный вами метод: ")

    parameters = {}
    while True:
        name = input("Введите параметр: ")  

        if not name:
            break

        value = input(f"Введите значение параметра: ")
        parameters[name] = value

    result = getattr(client.service, method)(**parameters)



if choice == "2":
    print(f"Доступные методы:")
    client = Client(url2)                                                                 
    methods = [method for method in dir(client.service) if not method.startswith('__')]

    for method in methods:
        print(f"+ {method}")

    method = input("Введите выбранный вами метод: ")

    parameters = {}
    while True:
        name = input("Введите параметр: ")  

        if not name:
            break

        value = input(f"Введите значение параметра: ")
        parameters[name] = value

    result = getattr(client.service, method)(**parameters)

else:
    print("Ошибка ввода")
