# steganography

r = 4

Для кодирования изображения 1 (image1) в изображение 2 (image2) введите команду: <br />
             python main.py merge --image1=image1.jpg --image2=image2.jpg --output=merged.png <br />
Для раскодирования изображения из другого изображения(из merged в unmerged) введите команду: <br />
             python main.py unmerge --image=merged.png --output=unmerged.png <br />


Тестовые изображения image1 и image2 находятся в папке вместе с main, программа работает долго в зависимости от размера картинки(кодирует на тестовом примере приблизительно за 7м, декодирует быстрее )<br />

В папках с _result содержатся примеры результатов работы кодирования и декодирования
