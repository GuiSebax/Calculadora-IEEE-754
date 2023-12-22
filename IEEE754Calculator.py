from decimal import Decimal

def binToInteger(bin: int) -> int:
    """Converte um numero em formato binario de sinal magnitude para inteiro"""
    strBin = str(bin)
    result = 0
    for i in range(len(strBin) - 1, -1, -1):
        if strBin[i] == "1":
            result += 2 ** (len(strBin) - (i + 1))
    return result

def integerToBin(num: int) -> str:
    """Converte um numero inteiro para binario em sinal magnitude"""
    binary = ""
    if num == 0:
        return "0"
    while num != 1:
        binary = f"{num % 2}{binary}"
        num = int(num / 2)
    binary = f"{num}{binary}"
    return binary

def decimalBinToFloat(bin: str) -> float:
    """Converte um numero binario representando uma parte decimal em ponto flutuante"""
    ans = 0
    
    for i in range(len(bin)):
        if bin[i] == '1':
           ans += pow((0.5), i + 1)
    return ans

def sumBinary(bin1: str, bin2: str) -> str:
    """Soma dois numeros binarios em sinal magnitude"""
    
    # Normalizando o tamanho dos numeros
    
    if len(bin1) > len(bin2):
        bin2 = bin2.zfill(len(bin1))
    else:
        bin1 = bin1.zfill(len(bin2))

    # Soma feita comparando bit a bit em cada um dos números e utilizando um carry:

    result = ""

    carry = 0

    for i in range(len(bin1) - 1, -1, -1):
        if bin1[i] == "0" and bin2[i] == "0":
            if carry == 1:
                result = f"1{result}"
                carry = 0
            else:
                result = f"0{result}"
        elif (bin1[i] == "1" and bin2[i] == "0") or (bin2[i] == "1" and bin1[i] == "0"):
            if carry == 0:
                result = f"1{result}"
            else:
                result = f"0{result}"
        else:
            if carry == 0:
                result = f"0{result}"
                carry = 1
            else:
                result = f"1{result}"

    if carry == 1:
        result = f"1{result}"

    return result


def subtractBinary(bin1: str, bin2: str) -> str:
    """Subtrai dois numeros binarios em sinal magnitude (OBS: bin1 deve ser maior que bin2 para a subtracao ser feita corretamente)"""
    
    # Adequando o tamanho dos numeros
    
    if len(bin1) > len(bin2):
        bin2 = bin2.zfill(len(bin1))
    else:
        bin1 = bin1.zfill(len(bin2))

    result = ""

    carry = 0
    
    # Subtração feita comparando bit a bit em cada um dos números e utilizando um carry:

    for i in range(len(bin1) - 1, -1, -1):
        if bin1[i] == "0" and bin2[i] == "0":
            if carry == 0:
                result = f"0{result}"
            else:
                result = f"1{result}"
        elif bin1[i] == "1" and bin2[i] == "0":
            if carry == 0:
                result = f"1{result}"
            else:
                result = f"0{result}"
                carry = 0
        elif bin2[i] == "1" and bin1[i] == "0":
            if carry == 0:
                result = f"1{result}"
                carry = 1
            else:
                result = f"0{result}"
                carry = 1
        else:
            if carry == 0:
                result = f"0{result}"
            else:
                result = f"1{result}"

    return result


def IEEEToFloat(bin: str, doublePrecision: int = 0) -> float:
    """Converte um numero no formato IEEE 754 para ponto flutuante, podendo estar em precisao simples ou dupla"""
    
    # Definindo sinal
    
    if (bin[0] == '1'):
        signal = -1
    else:
        signal = 1
    
    # Defninindo sinal do expoente e o valor a ser decrementado do expoente a partir da precisao do numero IEEE
    
    if(doublePrecision == 0):
        binExp = bin[1:9]
        if(greatestBinary(binExp, "01111111") == 1 or binExp == "01111111"):
            intExp = binToInteger(subtractBinary(binExp, "01111111"))
            expIsPositive = True
        else:
            intExp = binToInteger(subtractBinary("01111111", binExp))
            expIsPositive = False
            
        signify = '1' + bin[9:]
    else:
        binExp = bin[1:12]
        if(greatestBinary(binExp, "01111111111") == 1):
            intExp = binToInteger(subtractBinary(binExp, "01111111111"))
            expIsPositive = True
        else:
            intExp = binToInteger(subtractBinary("01111111111", binExp))
            expIsPositive = False
            
        signify = '1' + bin[12:]
        
    
    # Caso o expoente seja positivo, basta dividir o numero pelo index usando o valor do expoente para definir a parte inteira e decimal, no caso
    # do expoente ser negativo, o resultado terá necessariamente um valor 0 como inteiro, logo é definido de primeira o valor do inteiro e a
    # parte decimal é normalizada a partir do valor do expoente
    
    if(expIsPositive):
        
        # Caso o numero de digitos ultrapasse a quantidade representada, se faz necessário preencher os demais espaços com zero,
        # este fato pode ser diminuido aumentando a precisao da operação, porém aqui é trabalhado apenas precisão simples
        
        intSignify = signify.ljust(intExp + 1, '0')[:1 + intExp]
        decimalSignify = signify[1 + intExp:]
    else:
        intSignify = '0'
        decimalSignify = signify.zfill(len(signify) + (intExp - 1))

    # Convertendo de inteiro para decimal (parte inteira é convertida para Sinal Magnitude e a parte decimal com a conversão própria)
    
    intSignify = binToInteger(intSignify)
    decimalSignify = decimalBinToFloat(decimalSignify)
        
    return signal * ((intSignify + decimalSignify))
 



def multiplyBinary(bin1: str, bin2: str) -> str:
    """Multiplica dois numeros binarios em sinal magnitude, retornando o valor tambem em binario em sinal magnitude"""
    result = "0"
    
    # Método por soma a partir dos valores de '1' no multiplicando. Para cada '1' no multiplicando, é somado ao resultado final
    # o valor do multiplicador com o valor de zeros a direita a depender da posicao do '1' do multiplicando
    
    for i in range(0, len(bin1)):
        if(bin1[(len(bin1) - 1) - i] == "1"):
            valueToSum = bin2.ljust(len(bin2) + i, "0")
            result = sumBinary(result, valueToSum)

    return result

def divideBinary(bin1: str, bin2: str) -> str:
    """Divide dois numeros binarios em sinal magnitude, retornando um vetor onde na primeira posicao ha
    o quociente da divisao e na segunda posicao o resto da divisao, todos em resultados em sinal magnitude"""
    
    # Equalizando o tamanho dos numeros
    
    if(len(bin1) > len(bin2)):
        bin2 = bin2.zfill(len(bin1))
    else:
        bin1 = bin1.zfill(len(bin2))
        
    Q = "0"
    numerator = bin1
    
    print("Para efetuar uma divisao entre 2 numeros binarios, vamos utilizar o metodo de multiplas subtracoes.\n"
          "Neste metodo, efetuamos a subtracao entre o numerador e o denominador enquanto o restante da subtracao\n"
          "for maior que o denominador. Para cada subtracao efetuada, o quociente e incrementado em 1.\n"
          "Apos todas as subtracoes serem efetuadas, o quociente ja esta definido e o resto e adquirido pela\n"
          "operacao: numerador - (quociente * denominador)\n")
    
    # Metodo por subtracao do numerador até que o valor restante da subtracao seja menor que o denominador ou igual a zero.
    # Para cada iteracao realizada com sucesso, adicione 1 ao resultado do quociente
    
    while(greatestBinary(numerator, bin2) == 1 or bin2 == numerator.zfill(len(bin2))):
        numerator = subtractBinary(numerator, bin2)
        Q = sumBinary("1", Q)
    
    # Definindo o resto
    
    A = subtractBinary(bin1, multiplyBinary(bin2, Q))
    
    print("Ao efetuar as operacoes descritas acima, temos como resultado os seguintes valores:\n"
          f"Operacao {bin1} / {bin2} = {Q}, Resto = {A}\n")

    return [Q, A]

def divideBinaryFloat(bin1: str, bin2: str) -> str:
    """Divide dois numeros binarios no formato i.d, onde 'i' e 'd' sao numeros binarios, sendo 'i' a parte
    inteira e 'd' a parte decimal, retornando um numero no mesmo formato"""
    intPart1, decPart1 = bin1.split('.')
    intPart2, decPart2 = bin2.split('.')

    # Ajustando o numeros de digitos de cada numero
    
    if len(decPart1) > len(decPart2):
        decPart2 = decPart2.ljust(len(decPart1), '0')
    else:
        decPart1 = decPart1.ljust(len(decPart2), '0')
        
    bin1 = intPart1 + decPart1
    bin2 = intPart2 + decPart2
    
    # Efetuando divisao e separando o quociente do resto
    
    division = divideBinary(bin1, bin2)
    
    divisionQuocient = division[0]
    divisionRest = division[1]
    
    print("Com a divisao efetuada, temos o quociente e o resto. O quociente ja esta na representacao correta, porem\n"
          "a parte decimal tem uma representacao distinta. Cada bit na parte decimal representa o valor definido\n"
          "pela seguinte operacao: (0.5)^bitPos, onde bitPos signifca a posicao, da esquerda para a direita,\n"
          "iniciando a contagem a partir de 1, do bit no numero binario. Ao somar o valor que cada bit representa,\n"
          "temos o valor binario buscado\n")
    
    ans = divisionQuocient + '.'
    decPartFinal = ""
    numDecPlaces = 52
    
    print("Para transformar o resto binario encontrado na operacao anterior para o formato desejado, efetuamos o produto\n"
          "desse numero por 2 (que e a base binaria) e verificamos se o numero e maior que 1.\n"
          "Caso o numero seja maior que 1, e inserido '1' a direita do novo numero binario e subtraido 1 do numero binario,\n"
          "que fora multiplicado por 2, caso o resultado do produto seja menor que 1, e inserido '0' a direita do novo\n",
          "numero binario. Esse processo e efetuado ate o quao preciso queremos o numero, aqui, como o significando na\n"
          "precisao dupla tem 52 bits, essa e a quantidade de vezes que vamos efetuar a operacao para evitar erros.\n")
    
    counter = 0
    
    # Efetuando a conversão do resto em sinal magnitude para a representacao de binario decimal
    
    while(counter < numDecPlaces):
        divisionRest = multiplyBinary(divisionRest, "10")
        if(greatestBinary(divisionRest, bin2) == 1 or divisionRest == bin2):
            divisionRest = subtractBinary(divisionRest, bin2)
            decPartFinal += '1'
        else:
            decPartFinal += '0'
        counter += 1
    
    # ans já possui a parte inteira, basta adicionar a parte decimal calculada anteriormente
    
    ans = ans + decPartFinal
    
    print("Ao efetuar o processo anterior, temos a seguinte conversao:\n"
          f"Resto em representacao binaria regular: {divisionRest}\n"
          f"Resto em representacao binaria decimal: {decPartFinal}\n\n"
          "Com o valor decimal adquirido, basta coloca-lo a direita do ponto, separando da parte inteira parte inteira,\n"
          f"assim temos o resultado final como {ans}.\n")
    
    return ans

def greatestBinary(bin1: str, bin2: str) -> int:
    """Recebe dois numeros em sinal magnitude e verifica se bin1 e estritamente maior que bin2 (caso verdadeiro, retorna
    1, caso contrario retorna 0)"""
    
    # Equalizando o tamanho dos numeros
    
    if len(bin1) > len(bin2):
        bin2 = bin2.zfill(len(bin1))
    else:
        bin1 = bin1.zfill(len(bin2))

    # Verificando bits mais significativos
    
    for i in range(0, len(bin1)):
        if bin1[i] > bin2[i]:
            return 1
        elif bin1[i] < bin2[i]:
            return 0
    return 0


def floatToIEEE(num: float, doublePrecision: int = 0) -> str:
    """Converte um numero em ponto flutuante para a representacao IEEE 754, seja em precisao dupla ou nao"""
    
    # Verificando caso '0'
    
    if(num == float(0)):
        return '0'

    # Definindo sinal
    
    if num >= 0:
        signal = 0
    else:
        signal = 1
        num *= -1

    # Separando a parte inteira da decimal e convertendo a parte inteira para binário
    
    stringNum = str(Decimal(num)) # Utilizando a função Decimal() para remover a representacao exponencial "e+" ou "e-" em números muito grandes ou pequenos
    integerPart = int(stringNum.split('.')[0])
    decimalPart = num - integerPart
    integerBin = integerToBin(integerPart)
    
    decimalBin = ""
    
    # Para definir parte binaria, deve-se primeiro definir qual a precisao desejada
    
    if doublePrecision == 1:
        j = 64
        expoentSum = 1023
        leftZeroFill = 11
    else:
        j = 32
        expoentSum = 127
        leftZeroFill = 8
    
    # Convertendo binario em sinal magnitude para a representacao binaria da parte decimal
    
    for _ in range(j):
        decimalPart *= 2
        if(decimalPart >= 1.0):
            decimalBin += '1'
            decimalPart -= 1
        else:
            decimalBin += '0'
    
    # Juncao da parte inteira e decimal e remocao do ponto, salvando a posicao do ponto atual para o calculo do expoente
    
    binary = f"{integerBin}.{decimalBin}"
    
    binaryDotPosition = binary.index('.')

    binary = binary.replace('.', '')

    # Definindo a posicao do ponto no numero final para separar o bit oculto
    
    for k in range(0, j):
        if binary[k] == '1':
            dotFinalPos = k
            break
    
    # Remocao do bit oculto na representacao do significando
    
    binary = binary[k + 1:]
    
    # Calculo do expoente, que é a soma do valor da base a depender da precisao escolhida com a normalizacao a
    # partir da posicao do ponto na juncao das partes inteiras e binarias e a posicao para separar o bit oculto.
    # leftZeroFill é para caso o tamanho do numero nao seja adequado para a representacao desejada. Para
    # precisao simples, o tamanho é 8, já para precisao dupla é 11
    
    expoent = integerToBin((binaryDotPosition - (1 + dotFinalPos)) + expoentSum).zfill(leftZeroFill)
    
    # Juncao das partes do numero e limitando pela quantidade de bits que a representacao é composta a partir de 'j'

    result = f"{signal}{expoent}{binary}"[:j]
    
    return result


def sumOrSubtractIEEE(bin1: str, bin2: str, subtract: int) -> str:
    """
    Para subtract == 1, temos a operacao de subtracao, caso subtract == 0, temos a operacao de soma dos dois valores
    Tenha em mente que a ordem da operacao e feita como: "bin1 (operacao) bin2", ou seja, a ordem dos parametros e relevante
    """

    # Separando as partes do numero (Sinal, Expoente e Significando)
    
    newSignal = "0"
    i = 0

    signal1 = bin1[0]
    signal2 = bin2[0]

    expoent1 = bin1[1:9]
    expoent2 = bin2[1:9]
    
    signify1 = bin1[9:]
    signify2 = bin2[9:]
    
    print("Primeiro, separamos a representação do IEEE em suas respectivas partes: \n" + 
          f"Valor X: Sinal -> {signal1}; Expoente -> {expoent1}; Significando -> {signify1};\n" +
          f"Valor Y: Sinal -> {signal2}; Expoente -> {expoent2}; Significando -> {signify2};\n")

    # Caso os expoentes sejam distintos, verificar a magnitude
    
    if expoent1 != expoent2:

        # Equalizando os expoentes, normalizando o significando do numero com o expoente alterado
        
        # Caso o expoente do primeiro termo seja maior
        
        if greatestBinary(expoent1, expoent2):
            difference = binToInteger(subtractBinary(expoent1, expoent2))
            signify2 = signify2[: (len(signify2) - difference)].zfill(23)
            signify2 = signify2[: difference - 1] + "1" + signify2[difference:]
            signifyWithOcult1 = f"1{signify1}"
            signifyWithOcult2 = f"0{signify2}"
            expoent2 = expoent1
            newExpoent = expoent1

        # Caso o expoente do segundo termo seja maior
        
        else:
            difference = binToInteger(subtractBinary(expoent2, expoent1))
            signify1 = signify1[: (len(signify1) - difference)].zfill(23)
            signify1 = signify1[: difference - 1] + "1" + signify1[difference:]
            signifyWithOcult1 = f"0{signify1}"
            signifyWithOcult2 = f"1{signify2}"
            expoent1 = expoent2
            newExpoent = expoent2
            
    # Caso ambos os termos tenham os expoentes iguais
    
    else:
        newExpoent = expoent1
        signifyWithOcult1 = f"1{signify1}"
        signifyWithOcult2 = f"1{signify2}"

    print("Apos equalizar os expoentes em cada número e ajustando os significandos, temos\n" +
          "os seguintes novos significandos (Com os respectivos bits ocultos):\n" +
          f"Significando de X: {signifyWithOcult1}\n" +
          f"Significando de Y: {signifyWithOcult2}\n")

    # A depender da operação a ser executada, basta alterarmos o sinal do segundo termo
    
    if subtract == 1:
        signal2 = '1' if signal2 == '0' else '0'
        print("Como esta e uma operacao de subtracao, nos apenas trocamos\n" +
              f"o valor do sinal de Y de {0 if signal2 == 1 else 1} para {signal2}\n")
        
    # Definindo qual operação e qual sinal final da operacao a partir do sinal de cada numero

    print("Agora, iremos definir a operalçao a ser feita de acordo com os sinais recuperados anteriormente:\n" +
          "Sinal X == 0 and Sinal Y == 0 ---> Soma\n" +
          "Sinal X == 0 and Sinal Y == 1 ---> Subtracao\n" +
          "Sinal X == 1 and Sinal Y == 0 ---> Subtracao\n" +
          "Sinal X == 1 and Sinal Y == 1 ---> Soma\n")

    if signal1 == "0":
        if signal2 == "0":

            # Positivo com Positivo
            newSignify = sumBinary(signifyWithOcult1, signifyWithOcult2)
            newSignal = "0"
            
            print("Sinal X e Y == 0 --> Soma")
            print(f"Soma dos significandos: {newSignify}\nSinal final: {newSignal}\n")
        else:

            # Positivo com negativo
            
            print("Sinal X == 0 e Sinal Y == 1 --> Subtracao")

            if signifyWithOcult1 == signifyWithOcult2:
                print("Como os significandos são iguais em uma subtração, temos o resultado como 0\n")
                return "00000000000000000000000000000000"  # Como os sinais sao iguais, temos uma operacao de soma com sinais distintos de mesmo modulo, resultando em zero
            else:

                if greatestBinary(signifyWithOcult1, signifyWithOcult2) == 1:
                    newSignify = subtractBinary(signifyWithOcult1, signifyWithOcult2)
                    newSignal = "0"
                    print(f"Subtracao dos significandos: {newSignify}")
                else:
                    newSignify = subtractBinary(signifyWithOcult2, signifyWithOcult1)
                    newSignal = "1"
                    print(f"Subtracao dos significandos: {newSignify}")

                # Normalização do significando

                print("Agora fazemos a normalizacao dos significandos, ou seja, os zeros a esqueda sao removidos e\n" +
                      "entao decrementando o expoente de acordo\n")

                for i in range(0, len(newSignify)):

                    # Se o expoente for menor que o valor a ser decrementado para a normalizacao, temos um underflow no expoente

                    if greatestBinary(integerToBin(i), newExpoent) == 1:
                        print("Como o valor a ser decrementado do expoente e maior que o proprioe expoente\n" + 
                              "temos um caso de underflow, ou seja, nao podemos representar o expoente com a\n" + 
                              "precisao simples aqui utilizada\n")
                        return "Underflow!"

                    if newSignify[i] == "1":
                        newSignify = newSignify[i:].ljust(24, "0")
                        newExpoent = subtractBinary(newExpoent, integerToBin(i))
                        print("Apos a normalizacao temos os seguintes valores:\n" +
                              f"Significando: {newSignify}\nNovo expoente: {newExpoent}\n")
                        break

                print("Com a normalizacao feita, agora o sinal e definido a depender do numero de maior magnitude, que\n" +
                      f"neste caso, torna o nosso novo sinal igual para '{newSignal}'\n")
    else:
        if signal2 == "0":

            # Negativo com positivo
            
            print("Sinal X == 1 e Sinal Y == 0 --> Subtracao")

            if signifyWithOcult1 == signifyWithOcult2:
                print("Como os significandos são iguais em uma subtração, temos o resultado como 0\n")
                return "00000000000000000000000000000000"
            else:
                if greatestBinary(signifyWithOcult1, signifyWithOcult2) == 1:
                    newSignify = subtractBinary(signifyWithOcult1, signifyWithOcult2)
                    newSignal = "1"
                    print(f"Subtracao dos significandos: {newSignify}")
                else:
                    newSignify = subtractBinary(signifyWithOcult2, signifyWithOcult1)
                    newSignal = "0"
                    print(f"Subtracao dos significandos: {newSignify}")
                for i in range(0, len(newSignify)):

                    # Se o expoente for menor que o valor a ser decrementado para a normalizacao, temos um underflow no expoente

                    if greatestBinary(integerToBin(i), newExpoent) == 1:
                        print("Como o valor a ser decrementado do expoente e maior que o proprioe expoente\n" + 
                              "temos um caso de underflow, ou seja, nao podemos representar o expoente com a\n" + 
                              "precisao simples aqui utilizada\n")
                        return "Underflow!"

                    if newSignify[i] == "1":
                        newSignify = newSignify[i:].ljust(24, "0")
                        newExpoent = subtractBinary(newExpoent, integerToBin(i))
                        print("Apos a normalizacao temos os seguintes valores:\n" +
                              f"Significando: {newSignify}\nNovo expoente: {newExpoent}\n")
                        break

                print("Com a normalizacao feita, agora o sinal e definido a depender do numero de maior magnitude, que\n" +
                      f"neste caso, torna o nosso Sinal Final igual para '{newSignal}'\n")
        else:

            # Negativo com negativo

            newSignify = sumBinary(signifyWithOcult1, signifyWithOcult2)
            newSignal = "1"
            
            print("Sinal X e Y == 1 --> Soma")
            print(f"Soma dos significandos: {newSignify}\Sinal final: {newSignal}\n")

    # Adequando o significando e o expoente no caso da soma resultar em um significando com mais que 24 digitos 
    # (Incluindo o digito oculto)

    # Normalizando o numero com significando passando do limite da reprensentação do significando
    
    if len(newSignify) > 24:
        newExpoent = sumBinary(newExpoent, "1")
        print("Como o significando tem um tamanho maior que suportado pela representacao simples\n"
              "(25 contando com o bit oculto), omitimos um bit e somamos 1 ao expoente\n")

    # Verificando Overflow do expoente
    
    if len(newExpoent) > 8:
        print("Apos a soma no expoente, o expoente passou a precisar de 9 bits para armazenar o resultado,"
                "porem na representacao simples, ha apenas 8 bits para armazenamento, levando a um overflow.\n")
        return "Overflow!"

    newSignify = newSignify[1:]
    
    print("Valores encontrados apos as operacoes:\n" +
          f"Sinal Final -> {newSignal}; Expoente -> {newExpoent}; Significando: {newSignify}\n")

    result = f"{newSignal}{newExpoent}{newSignify}"[:32]

    return result


def multiplyIEEE(bin1: str, bin2: str) -> str:
    """Efetua o produto entre dois numeros no formato IEEE 754 de precisao simples, retornando um numero no formato
    IEEE 754 de precisao dupla"""
    
    # Separando os significandos dos expoentes
    
    signify1 = "1" + bin1[9:]
    signify2 = "1" + bin2[9:]
    
    exp1 = bin1[1:9]
    exp2 = bin2[1:9]
    
    print("Primeiro, separamos a representação do IEEE em suas respectivas partes: \n" + 
        f"Valor X: Sinal -> {bin1[0]}; Expoente -> {exp1}; Significando -> {signify1};\n" +
        f"Valor Y: Sinal -> {bin2[0]}; Expoente -> {exp2}; Significando -> {signify2};\n")

    # Como os expoentes estão representados em Sinal Magnitude, não há como verificar se a operação resultará em um valor positivo
    # ou negativo, então a verificação do sinal é feita manualmente
    
    if(greatestBinary(exp1, "1111111") == 1):
        
        print(f"Para o expoente X, como {exp1} > 1111111, temos que o expoente de X e positivo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp1 = subtractBinary(bin1[1:9], "1111111")
        exp1IsPositive = True
    else:
        
        print(f"Para o expoente X, como {exp1} < 1111111, temos que o expoente de X e negativo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp1 = subtractBinary("1111111", bin1[1:9])
        exp1IsPositive = False
    
    if(greatestBinary(exp2, "1111111") == 1):
        
        print(f"Para o expoente Y, como {exp2} > 1111111, temos que o expoente de X e positivo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp2 = subtractBinary(bin2[1:9], "1111111")
        exp2IsPositive = True
    else:
        
        print(f"Para o expoente X, como {exp2} < 1111111, temos que o expoente de X e negativo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp2 = subtractBinary("1111111", bin2[1:9])
        exp2IsPositive = False
    
    if(greatestBinary(exp1, exp2) == 1):
        if(exp1IsPositive and exp2IsPositive):
            newExp = sumBinary(exp1, exp2)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| > |Expoente Y|) e ambos positivos, temos o \n"
                  f"expoente resultante da soma de ambos os numeros como +{newExp}\n")
            
        elif(exp1IsPositive and not exp2IsPositive):
            newExp = subtractBinary(exp1, exp2)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| > |Expoente Y|) com Expoente X positivo e Y negativo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
            
        elif(not exp1IsPositive and exp2IsPositive):
            newExp = subtractBinary(exp1, exp2)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| > |Expoente Y|) com Expoente X negativo e Y positivo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como -{newExp}\n")
            
        else:
            newExp = sumBinary(exp1, exp2)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| > |Expoente Y|) e ambos negativos, temos o \n"
                  f"expoente resultante da soma de ambos os numeros como -{newExp}\n")
            
    else:
        if(exp2IsPositive and exp1IsPositive):
            newExp = sumBinary(exp2, exp1)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| < |Expoente Y|) e ambos positivos, temos o \n"
                  f"expoente resultante da soma de ambos os numeros como +{newExp}\n")
            
        elif(exp2IsPositive and not exp1IsPositive):
            newExp = subtractBinary(exp2, exp1)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| < |Expoente Y|) com Expoente X negativo e Y positivo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
            
        elif(not exp2IsPositive and exp1IsPositive):
            newExp = subtractBinary(exp2, exp1)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| < |Expoente Y|) com Expoente X positivo e Y negativo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como -{newExp}\n")
            
        else:
            newExp = sumBinary(exp2, exp1)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| < |Expoente Y|) e ambos negativos, temos o \n"
                  f"expoente resultante da soma de ambos os numeros como -{newExp}\n")
            

    # A depender do sinal, a operação deve ser alterada para o módulo correto se manter, ai o sinal do expoente estará armazenado
    # na variável "newExpIsPositive", que será utilizado mais a frente
    
    if(newExpIsPositive):
        newExp = sumBinary(newExp, "1111111111").zfill(11)
    else:
        newExp = subtractBinary("1111111111", newExp).zfill(11)

    print("Para definirmos o expoente, primeiro subtraimos '1111111' de cada um dos expoentes:\n" +
          f"Expoente X -> {exp1}\n" +
          f"Expoente Y -> {exp2}\n" +
          "Com os valores dos expoentes em sua forma binaria direta, basta soma-los juntamente com '1111111111'\n" +
          "(Como a representacao e de dupla precisao, '1111111111' e o valor somado ja que o expoente deve ter 11 bits para ser representado)\n" +
          f"Com isso, temos {exp1} + {exp2} + 1111111111 = {newExp}\n")

    # Verificando caso de Overflow
    
    if(len(newExp) > 11):
        print("Com a soma anterior resultou em um expoente de tamanho maior que 11 bits, nao podemos armazena-lo nessa representacao, logo temos\n" +
              "um overflow\n")
        return "Overflow!"

    # Produto dos significandos
    
    signify = multiplyBinary(signify1, signify2)

    # Verificando necessidade de normalizar o expoente por conta do produto dos significandos
    
    if(len(signify) == len(signify1) + len(signify2)):
        print("Por conta do tamanho do significando resultante do produto ter o mesmo tamanho da soma do tamanho dos outros\n"
              "2 significandos, ocorre um deslocamento do bit oculto, onde um 0 invade a area delimitada para o bit oculto,"
              "para arrumar esse problema, e somado '1' ao expoente para deslocar o ponto uma casa para a esquerda,"
              f"assim a representacao esta correta. Com isso temos o novo expoente como {newExp} + 1 = {sumBinary(newExp, '1')}\n")
        newExp = sumBinary(newExp, "1")
    
    # Ajustando o significando em caso da representação não ser completamente preenchida
    
    signify = signify.ljust(53, '0')
    
    print(f"Para a multiplicacao, o metodo utilizado se baseia em somar o valor do multiplicador ({signify2}) baseando-se nos valores\n" +
          f"do multiplicando ({signify1}) da seguinte maneira:\n" +
          "Para cada bit do multiplicando, do menos significativo para o mais significativo, caso ele seja '1', o valor do multiplicador e somado\n" +
          "para o produto final. Porem, para cada bit analisado, um bit de '0' deve ser adicionado a direito do multiplicador, para manter a relacao\n" +
          "de significancia dos valores.\n" +
          f"Dessa forma, temos {signify1} * {signify2} = {signify}.\n")
    
    # Definindo o sinal
    
    if(bin1[0] == bin2[0]):
        signal = "0"
        print("Por fim, verificamos o sinal dos numeros, como os sinais sao iguais, o sinal final e positivo (0).\n")
    else:
        signal = "1"
        print("Por fim, verificamos o sinal dos numeros, como os sinais sao distintos, o sinal final e negativo (1).\n")
    
    print("Agora, analisando o sinal, basta verificar se os sinais sao iguais ou distintos. Caso sejam iguais, significa que o sinal sera\n" +
          f"positivo (1), caso contrario, o sinal sera negativo (1): X -> {bin1[0]} e Y -> {bin2[0]} => {signal}")

    print("Valores encontrados apos as operacoes:\n" +
        f"Sinal Final -> {signal}; Expoente -> {newExp}; Significando: {signify} (Com o bit oculto)\n")
        
    result = f"{signal}{newExp}{signify[1:]}"[:64]
    
    return result

def divideIEEE(bin1: str, bin2: str) -> str:
    """Realiza a divisao entre dois numeros binarios no formato IEEE 754 de precisao simples, retornando um numero no formato
    IEEE 754 de precisao dupla """
    
    # Verificando casos de divisão por zero ou divisão de um numerador igual a zero
    
    if(bin2 == '0'*len(bin2)):
        print("Divisao por zero nao pode ser definida!\n")
        return "Invalido"
    
    elif(bin1 == '0'*len(bin1)):
        print("Como o numerador e o proprio numero zero, o resultado sera zero para qualquer outro valor no denominador\n")
        return '0'*len(bin1)

    # Separando significando e expoente
    
    norm1 = '1.' +  bin1[9:]
    norm2 = '1.' + bin2[9:]
    
    exp1 = bin1[1:9]
    exp2 = bin2[1:9]
    
    print(f"Primeiro, separamos o expoente das demais partes do numero:\nExpoente de X -> {exp1}\nExpoente de Y -> {exp2}\n")
    
    # Como os expoentes estão representados em Sinal Magnitude, não há como verificar se a operação resultará em um valor positivo
    # ou negativo, então a verificação do sinal é feita manualmente 
    
    if(greatestBinary(exp1, "1111111") == 1):
        
        print(f"Para o expoente X, como {exp1} > 1111111, temos que o expoente de X e positivo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp1 = subtractBinary(bin1[1:9], "1111111")
        exp1IsPositive = True
    else:
        
        print(f"Para o expoente X, como {exp1} < 1111111, temos que o expoente de X e negativo, logo temos que levar isso\n"
              "em consideracao ao calcular o expoente da operacao\n")
        
        exp1 = subtractBinary("1111111", bin1[1:9])
        exp1IsPositive = False
    
    if(greatestBinary(exp2, "1111111") == 1):
        
        print(f"Para o expoente Y, como {exp2} > 1111111, temos que o expoente de Y e positivo, logo temos que levar isso\n"
            "em consideracao ao calcular o expoente da operacao\n")
        
        exp2 = subtractBinary(bin2[1:9], "1111111")
        exp2IsPositive = True
    else:
        
        print(f"Para o expoente Y, como {exp2} < 1111111, temos que o expoente de Y e negativo, logo temos que levar isso\n"
            "em consideracao ao calcular o expoente da operacao\n")
        
        exp2 = subtractBinary("1111111", bin2[1:9])
        exp2IsPositive = False
    
    if(greatestBinary(exp1, exp2) == 1):
        if(exp1IsPositive and exp2IsPositive):            
            newExp = subtractBinary(exp1, exp2)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| > |Expoente Y|) e ambos positivos, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")

        elif(exp1IsPositive and not exp2IsPositive):
            newExp = sumBinary(exp1, exp2)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| > |Expoente Y|) com Expoente de X positivo e de Y negativo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
            
        elif(not exp1IsPositive and exp2IsPositive):
            newExp = sumBinary(exp1, exp2)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| > |Expoente Y|) com Expoente de X negativo e de Y positivo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como -{newExp}\n")
            
        else:
            newExp = subtractBinary(exp1, exp2)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| > |Expoente Y|) e ambos negativos, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
            
    else:
        if(exp2IsPositive and exp1IsPositive):
            newExp = subtractBinary(exp2, exp1)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| < |Expoente Y|) e ambos positivos, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como -{newExp}\n")
            
        elif(exp2IsPositive and not exp1IsPositive):
            newExp = sumBinary(exp2, exp1)
            newExpIsPositive = False
            
            print("Tendo (|Expoente X| < |Expoente Y|) com Expoente X negativo e Y positivo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como -{newExp}\n")
            
        elif(not exp2IsPositive and exp1IsPositive):
            newExp = sumBinary(exp2, exp1)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| < |Expoente Y|) com Expoente X positivo e Y negativo, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
            
        else:
            newExp = subtractBinary(exp2, exp1)
            newExpIsPositive = True
            
            print("Tendo (|Expoente X| < |Expoente Y|) e ambos negativos, temos o \n"
                  f"expoente resultante da subtracao de ambos os numeros como +{newExp}\n")
    temp = newExp
    
    if(newExpIsPositive):            
        newExp = sumBinary(newExp, "1111111111").zfill(11)
        print("Como o resultado da subtracao dos expoentes e positivo, efetuamos a operacao de soma\n"
              f"para definir o novo expoente: {temp} + 1111111111 = {newExp}\n")
        
    else:
        newExp = subtractBinary("1111111111", newExp).zfill(11)
        print("Como o resultado da subtracao dos expoentes e negativo, efetuamos a operacao de subtracao\n"
              f"para definir o novo expoente: 1111111111 - {temp} = {newExp}\n")
    
    print("Com o expoente em maos, seguimos para o calculo da divisao dos significandos:\n"
          f"Significando de X: {norm1} (Com bit oculto)\n"
          f"Significando de Y: {norm2} (Com bit oculto)\n")
    
    # Efetuando a divisão dos significandos, há de se lembrar que signify[0] se refere ao quociente e signify[1] ao resto da divisão
    
    signify = divideBinaryFloat(norm1, norm2)
    
    # Como se a divisão ter quociente zero temos certeza que o resto começará com '1', já que os zeros a esquerda são removidos, basta
    # deslocar o ponto uma casa a direita. No processo abaixo o bit oculto já é removido da representação
    
    if(signify[0] == '0'):
        print("Como o resultado da divisao possui a parte inteira igual a 0, deslocamos o ponto uma casa para a direita,"
              "normalizando o numero e decrementamos o expoente em 1 unidade.")
        signify = signify[signify.index('.') + 2:].ljust(53, '0')
        newExp = subtractBinary(newExp, '1')
    else:
        signify = signify[signify.index('.') + 1:].ljust(53, '0')
            
    print("Apos remover o bit oculto da representacao do significando, temos o\n"
          f"novo significando como {signify}")
    
    # Definindo o sinal
    
    if(bin1[0] == bin2[0]):
        signal = "0"
        print("Por fim, verificamos o sinal dos numeros, como os sinais sao iguais, o sinal final e positivo (0).\n")
    else:
        signal = "1"
        print("Por fim, verificamos o sinal dos numeros, como os sinais sao distintos, o sinal final e negativo (1).\n")

    # Junção de todas as partes
    
    print("Finalmente, temos as seguintes partes do numero no formato IEEE 754:\n"
          f"Sinal: {signal}; Expoente: {newExp}; Significando (sem bit oculto): {signify}\n")
    result = f"{signal}{newExp}{signify}"[:64]
    
    return result


# Função de inicialização do programa, a qual faz a chamadas das operações e requisita os valores do usuário.

def initialize() -> None:
    operation = input(
        "Informe a operacao a ser efetuada\n"
        "1) Soma (+)\n"
        "2) Subtracao (-)\n"
        "3) Multiplicao (*)\n"
        "4) Divisao (/)\n"
        "5) Sair\n"
        "Opcao: "
    )
    
    if(operation == '5'):
        exit(0)
    
    value1 = float(input("Insira o primeiro valor da operacao (X): "))
    value2 = float(input("Insira o primeiro valor da operacao (Y): "))

    convertedValue1 = floatToIEEE(value1)
    convertedValue2 = floatToIEEE(value2)
    
    print(f"Representação do valor X {value1} em IEEE 754 -> {convertedValue1}\n" + 
          f"Representação do valor Y {value2} em IEEE 754 -> {convertedValue2}\n")

    if(operation == '1'):
        ans = sumOrSubtractIEEE(convertedValue1, convertedValue2, 0)
        
        print(f"Resultados:\n| Valor X{''.ljust(23)}| Valor Y{''.ljust(23)}| Resposta")
        
        if(ans != "Overflow!" or ans != "Underflow!"):
            print(f"{str(value1).ljust(32)} + {str(value2).ljust(32)} = {IEEEToFloat(ans)}")
        
        else:
            print(f"{str(value1).ljust(32)} + {str(value2).ljust(32)} = {ans}")
        
        print(f"{convertedValue1} + {convertedValue2} = {ans}\n")
        initialize()
        
    if(operation == '2'):
        ans = sumOrSubtractIEEE(convertedValue1, convertedValue2, 1)
        
        print(f"Resultados:\n| Valor X{''.ljust(23)}| Valor Y{''.ljust(23)}| Resposta")
        
        if(ans != "Overflow!" or ans != "Underflow!"):
            print(f"{str(value1).ljust(32)} - {str(value2).ljust(32)} = {IEEEToFloat(ans)}")
        
        else:
            print(f"{str(value1).ljust(32)} - {str(value2).ljust(32)} = {ans}")
        
        print(f"{convertedValue1} - {convertedValue2} = {ans}\n")
        initialize()

    if(operation == '3'):
        ans = multiplyIEEE(convertedValue1, convertedValue2)
        
        print(f"Resultados:\n| Valor X{''.ljust(23)}| Valor Y{''.ljust(23)}| Resposta")
        
        if(ans != "Overflow!"):
            print(f"{str(value1).ljust(32)} * {str(value2).ljust(32)} = {IEEEToFloat(ans, 1)}")
        
        else:
            print(f"{str(value1).ljust(32)} * {str(value2).ljust(32)} = {ans}")
        
        print(f"{convertedValue1} * {convertedValue2} = {ans}\n")
        initialize()
        
    if(operation == '4'):
        ans = divideIEEE(convertedValue1, convertedValue2)
        
        print(f"Resultados:\n| Valor X{''.ljust(23)}| Valor Y{''.ljust(23)}| Resposta")
        
        if(ans != "Overflow!" and ans != '0'*len(convertedValue1) and ans != "Invalido"):
            print(f"{str(value1).ljust(32)} / {str(value2).ljust(32)} = {IEEEToFloat(ans, 1)}")
        
        else:
            print(f"{str(value1).ljust(32)} / {str(value2).ljust(32)} = {ans}")
        
        print(f"{convertedValue1} / {convertedValue2} = {ans}\n")
        initialize()


if __name__ == "__main__":

    initialize()