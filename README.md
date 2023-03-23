# steganography

r = 4

Для кодирования изображения 1 (image1) в изображение 2 (image2) введите команду:
             python main.py merge --image1=image1.jpg --image2=image2.jpg --output=merged.png
Для раскодирования изображения из другого изображения(из merged в unmerged) введите команду:
             python main.py unmerge --image=merged.png --output=unmerged.png


Тестовые изображения image1 и image2 находятся в папке main, программа работает долго в зависимости от размера картинки(кодирует на тестовом примере приблизительно за 7м, декодирует быстрее )
