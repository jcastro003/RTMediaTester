import RPi.GPIO as GPIO
import time


#mapeamento do LCD na GPIO
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18


#Constantes de LCD
LCD_WIDTH = 20
LCD_CHR   = True
LCD_CMD   =  False

LCD_LINE_1 = 0x80 # Endereço do LCD na RAM
LCD_LINE_2 = 0xC0 # Endereço do LCD na RAM
LCD_LINE_3 = 0x94 # Endereço do LCD na RAM
LCD_LINE_4 = 0xD4 # Endereço do LCD na RAM

#Constantes de tempo
E_PULSE = 0.005
E_DELAY = 0.005

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


# Config
    pins = [2,3,4,17,27,22]


# GPIO Setup
    for pin in pins:
     GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# use P1 header pin numbering convention

	# Wait
    time.sleep(0.03)

    i = 1
	# lazy not bit smashing
    output = ''
    for pin in pins:
     # inverted
     if not GPIO.input(pin):
      output += '1'
     else:
      output += '0'
    i += 1

	# reverse the output string
    output = output[::-1]
	

    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    lcd_init()

    if output == '000000':
     lcd_byte(LCD_LINE_1, LCD_CMD)
     lcd_string("------------------",2)
     lcd_byte(LCD_LINE_2, LCD_CMD)
     lcd_string("Teste com audio",2)
     lcd_byte(LCD_LINE_4, LCD_CMD)
     lcd_string("------------------",2)

    elif output == '000001':
     lcd_byte(LCD_LINE_1, LCD_CMD)
     lcd_string("------------------",2)
     lcd_byte(LCD_LINE_2, LCD_CMD)
     lcd_string("Teste com imagem",2)
     lcd_byte(LCD_LINE_4, LCD_CMD)
     lcd_string("------------------",2)

    elif output == '000011':
     lcd_byte(LCD_LINE_1, LCD_CMD)
     lcd_string("------------------",2)
     lcd_byte(LCD_LINE_2, LCD_CMD)
     lcd_string("Teste com video",2)
     lcd_byte(LCD_LINE_4, LCD_CMD)
     lcd_string("------------------",2)
    else:
     lcd_byte(LCD_LINE_1, LCD_CMD)
     lcd_string("------------------",2)
     lcd_byte(LCD_LINE_2, LCD_CMD)
     lcd_string("Configuração Inválida",2)
     lcd_byte(LCD_LINE_4, LCD_CMD)
     lcd_string("------------------",2)




def lcd_init():
  # Initialise display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)



def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)

if __name__ == '__main__':
    main()
