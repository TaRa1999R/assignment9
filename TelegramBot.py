import random
import telebot
from telebot import types
from khayyam import JalaliDate
import gtts
import qrcode

#----------------------------------------------------------------------------------------------- moteqayer

mode = " "
computer_number = " "
bot = telebot.TeleBot ( "5902045314:AAEHPSgekMmYUsuyfkZpD3HiG1t2KSyr-z8" , parse_mode = None )

#----------------------------------------------------------------------------------------------- keyboard

main_keyboard = types.ReplyKeyboardMarkup ( row_width = 3 ) 
key1 = types.KeyboardButton (" /game ")
key2 = types.KeyboardButton (" /age ")
key3 = types.KeyboardButton (" /voice ")
key4 = types.KeyboardButton (" /max ")
key5 = types.KeyboardButton (" /argmax ")
key6 = types.KeyboardButton (" /QR_code ")
main_keyboard.add ( key1 , key2 , key3 , key4 , key5 , key6 )

game_keyboard = types.ReplyKeyboardMarkup ( row_width = 1 )
key7 = types.KeyboardButton (" /New_game ")
key8 = types.KeyboardButton (" /Exit ")
game_keyboard.add ( key7 , key8 )

back_keybord = types.ReplyKeyboardMarkup ( row_width = 1 )
key9 = types.KeyboardButton (" /return ")
back_keybord.add ( key9 )

#-------------------------------------------------------------------------------------------------- command haye asli

@bot.message_handler ( commands = ["start"] )
def welcome ( message ) :
    bot.reply_to ( message, message.from_user.first_name + " به بات من خوش اومدی " )
    bot.send_message ( message.chat.id , " برای دیدن توضیحات هر گزینه از کامند 'help' استفاده کنید " , reply_markup = main_keyboard )


@bot.message_handler ( commands = ["help"] )
def information ( message ) :
    bot.send_message ( message.chat.id , " game : بازی حدس عدد " )
    bot.send_message ( message.chat.id , " age : تبدیل تاریخ تولد به سن " )
    bot.send_message ( message.chat.id , " voice : تبدیل متن با فایل صوتی " )
    bot.send_message ( message.chat.id , " max : اعلام بزرگترین عدد موجود در مجموعه " )
    bot.send_message ( message.chat.id , " argmax : اعلام اندیس بزرگترین عدد موجود در مجموعه " )
    bot.send_message ( message.chat.id , " QR code : کد QR تولید " , reply_markup = main_keyboard )

@bot.message_handler ( commands = ["return" , "Exit"] )
def back_to_menue ( message ) :
   bot.send_message ( message.chat.id , " بازکشت به منوی اصلی " , reply_markup = main_keyboard )
   mode = " "

#----------------------------------------------------------------------------------------------------- command haye menue

@bot.message_handler ( commands = ["game" , "New_game"] )
def game_mode ( message ) :
  global mode
  global computer_number
  bot.reply_to ( message , " عدد مورد نظر من بین 0 تا 100 🤐 می تونی عدد رو حدس بزنی ؟؟ 🤔 "  )
  computer_number = random.randint ( 0 , 100 )
  bot.send_message ( message.chat.id , " شروع کن " , reply_markup = game_keyboard )
  mode = "game"

@bot.message_handler ( commands = ["age"] )
def age_mode ( message ) :
  global mode
  bot.reply_to ( message , " تاریخ تولد خود را به صورت هجری شمسی به شکل زیر بنوریس " )
  bot.send_message ( message.chat.id , " yyyy/mm/dd " , reply_markup = back_keybord )
  mode = "age"

@bot.message_handler ( commands = ["voice"] )
def voice_mode ( message ) :
  global mode 
  bot.reply_to ( message , " لطفا متن مورد نظر خود را وارد کنید " )
  bot.send_message ( message.chat.id , " متن باید به زبان انگلیسی باشد " , reply_markup = back_keybord )
  mode = "voice"

@bot.message_handler ( commands = ["max"] )
def voice_mode ( message ) :
  global mode 
  bot.reply_to ( message , " لازم است مجموعه ای از اعداد وارد کن " )
  bot.send_message ( message.chat.id , " بین هر دو عدد یک ویرگول قرار بده " , reply_markup = back_keybord )
  mode = "max"

@bot.message_handler ( commands = ["argmax"] )
def voice_mode ( message ) :
  global mode 
  bot.reply_to ( message , " لازم است مجموعه ای از اعداد را وارد کن " )
  bot.send_message ( message.chat.id , " بین هر دو عدد یک ویرگول قرار بده " , reply_markup = back_keybord )
  mode = "argmax"

@bot.message_handler ( commands = ["QR_code"] )
def voice_mode ( message ) :
  global mode 
  bot.reply_to ( message , " اطلاعاتی که میخواهی در غالب یک QRCode ذخیره کنی را وارد کن " )
  bot.send_message ( message.chat.id , " اطلاعات می تواند به هر زبانی باشد " , reply_markup = back_keybord )
  mode = "QR_code"

#------------------------------------------------------------------------------------------------------ main

@bot.message_handler ( func = lambda m : True )
def play_game ( message ) :
    global mode
    global computer_number
    
    if mode == "game" :
      user_guess = int ( message.text )

      if user_guess > computer_number :
        bot.reply_to ( message , " زیاده بابا 😅 بیا پایین ⏬⬇ " )

      elif user_guess < computer_number :
        bot.reply_to ( message , " کمه بابا 😅 بیا بالا ⏫⬆ " )

      elif user_guess == computer_number :
        bot.reply_to ( message , " 🎉 آفرین برنده  شدی 🎉 " )
        bot.send_message ( message.chat.id , " خب حالا چی ؟ " , reply_markup = main_keyboard)
        mode = " "

    elif mode == "age" :
      birth_date = message.text.split ("/")
      year = int ( birth_date [0] )
      month = int ( birth_date [1] )
      day = int (birth_date [2] )
      difference = JalaliDate.today () - JalaliDate ( year , month , day )
      Difference = str( difference ).split(" ")
      rooz = int ( Difference[0] )
      sal = int ( rooz / 365 )
      text = " تو " + str (sal) + " سال سن داری "
      bot.send_message ( message.chat.id , text , reply_markup = main_keyboard )
      mode = " "

    elif mode == "voice" :
      user_text = ( message.text )
      sound = gtts.gTTS ( user_text , lang = "en" , slow = False )
      sound.save ( "sound.mp3" )
      voice = open ( "sound.mp3" , "rb")
      bot.send_voice ( message.chat.id , voice , reply_markup = main_keyboard )
      mode = " "

    elif mode == "max" :
      array = []
      user_input = message.text.split (",")
      for number in user_input :
        array.append ( int ( number ) )
      Array = sorted ( array )
      text = " بزرگترین عدد در این مجموعه " + str ( Array [ len ( array ) - 1]) + " است "
      bot.send_message ( message.chat.id , text , reply_markup = main_keyboard )
      mode = " "
      
    elif mode == "argmax" :
      array = []
      user_input = message.text.split (",")
      for number in user_input :
        array.append ( int ( number ))
      max_number = array[0]
      index = 0
      for i in range ( 1 , len ( array )) :
        if max_number <= array [ i ] :
          max_number = array [ i ]
          index = i
      text = " بزرگترین عدد در این مجموعه دارای اندیس " + str ( index ) + " است "
      bot.send_message ( message.chat.id , text , reply_markup = main_keyboard )
      mode = " "

    elif mode == "QR_code" :
      user_input = ( message.text)
      qr_photo = qrcode.make ( user_input )
      qr_photo.save ( "qr_photo.png" )
      aks = open ( "qr_photo.png" , "rb" )
      bot.send_photo ( message.chat.id , aks , reply_markup = main_keyboard )
      mode = " "

bot.infinity_polling ()