from PIL import Image
import numpy as np
import argparse


class Steganography:
    BLACK_PIXEL = (0, 0, 0)
    H = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])

    def arr_to_str(self, arr):
        res = ''
        for x in arr:
            for el in x:
                res += str(el)
        return res

    def str_to_arr(self, s):
        res = []
        for c in s:
            res.append([int(c)])
        return res

    # получить из массива индекс
    def get_ind(self, arr):
        s = ''
        for c in arr:
            for x in c:
                s += str(x)
        return int(s, 2)

    # матрицу в 2-ный вид
    def matr_to_bin(self, m):
        for x in m:
            x %= 2
        return m

    # поменять бит по индексу  контейнере
    def set_bit(self, container, ind):
        if ind <= 0 or ind > len(container):
            return container
        if container[ind - 1][0] == 1:
            container[ind - 1][0] = 0
        else:
            container[ind - 1][0] = 1
        return container

    def _int_to_bin(self, rgb):
        """Преобразовывает целочисленный кортеж в двоичный (строковый) кортеж.

        :param rgb: Целочисленный кортеж подобный (220, 110, 96)
        :return: Строковый кортеж, подобный ("00101010", "11101011", "00010110")
        """
        r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        """Преобразовывает двоичный (строковый) кортеж в целочисленный кортеж.

        :param rgb: Строковый кортеж, подобный ("00101010", "11101011", "00010110")
        :return: Целочисленный кортеж подобный (220, 110, 96)
        """
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb_sm):
        """Объединить 5 кортежей RGB

        :param rgb1: Целочисленный кортеж вида (220, 110, 96) первой картинки
        :param rgb2: Целочисленный кортеж вида (220, 110, 96) первой картинки
        :param rgb3: Целочисленный кортеж вида (220, 110, 96) первой картинки
        :param rgb4: Целочисленный кортеж вида (220, 110, 96) первой картинки
        :param rgb_sm: Целочисленный кортеж вида (220, 110, 96) второй картинки
        :return: An integer tuple with the two RGB values merged.
        """

        # в каждой переменной лежит строка из 8 бит
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        r_sm, g_sm, b_sm = self._int_to_bin(rgb_sm)

        # получили 3 контейнера по 15 элементов
        container_r = np.array(self.str_to_arr(r1[-3:] + r2[-4:] + r3[-4:] + r4[-4:]))
        container_g = np.array(self.str_to_arr(g1[-3:] + g2[-4:] + g3[-4:] + g4[-4:]))
        container_b = np.array(self.str_to_arr(b1[-3:] + b2[-4:] + b3[-4:] + b4[-4:]))

        # m - что нам нужно закодировать (r g b - цвета)
        m_r = np.array(self.str_to_arr(r_sm[:4]))
        m_g = np.array(self.str_to_arr(g_sm[:4]))
        m_b = np.array(self.str_to_arr(b_sm[:4]))

        # умножили H * container  и привели в бинарный вид
        mul_rh = self.matr_to_bin(np.dot(self.H, container_r))
        mul_gh = self.matr_to_bin(np.dot(self.H, container_g))
        mul_bh = self.matr_to_bin(np.dot(self.H, container_b))

        # вычли m - H*cont  -- получили номер ошибки
        sub_r = self.matr_to_bin(m_r - mul_rh)
        sub_g = self.matr_to_bin(m_g - mul_gh)
        sub_b = self.matr_to_bin(m_b - mul_bh)

        # во всех контейнерах меняем нужные биты
        cont_r = self.arr_to_str(self.set_bit(container_r, self.get_ind(sub_r)))
        cont_g = self.arr_to_str(self.set_bit(container_g, self.get_ind(sub_g)))
        cont_b = self.arr_to_str(self.set_bit(container_b, self.get_ind(sub_b)))

        # пиксели  готовы к прорисовке
        nr1, nr2, nr3, nr4 = r1[:5] + cont_r[0:3], r2[:4] + cont_r[3:7], r3[:4] + cont_r[7:11], r4[:4] + cont_r[11:]
        ng1, ng2, ng3, ng4 = g1[:5] + cont_g[0:3], g2[:4] + cont_g[3:7], g3[:4] + cont_g[7:11], g4[:4] + cont_g[11:]
        nb1, nb2, nb3, nb4 = b1[:5] + cont_b[0:3], b2[:4] + cont_b[3:7], b3[:4] + cont_b[7:11], b4[:4] + cont_b[11:]

        rgb1 = nr1, ng1, nb1
        rgb2 = nr2, ng2, nb2
        rgb3 = nr3, ng3, nb3
        rgb4 = nr4, ng4, nb4

        arr = [self._bin_to_int(rgb1), self._bin_to_int(rgb2), self._bin_to_int(rgb3), self._bin_to_int(rgb4)]

        # rgb = r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4]
        # return self._bin_to_int(rgb)
        return arr

    def _unmerge_rgb(self, rgb1, rgb2, rgb3, rgb4):
        """Unmerge RGB.

        :param rgbn: Целочисленный кортеж типа (220, 110, 96)
        :return: Целочисленный кортеж с объединенными 5 значениями RGB.
        """
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)

        container_r = np.array(self.str_to_arr(r1[-3:] + r2[-4:] + r3[-4:] + r4[-4:]))
        container_g = np.array(self.str_to_arr(g1[-3:] + g2[-4:] + g3[-4:] + g4[-4:]))
        container_b = np.array(self.str_to_arr(b1[-3:] + b2[-4:] + b3[-4:] + b4[-4:]))

        mul_rh = self.arr_to_str(self.matr_to_bin(np.dot(self.H, container_r)))
        mul_gh = self.arr_to_str(self.matr_to_bin(np.dot(self.H, container_g)))
        mul_bh = self.arr_to_str(self.matr_to_bin(np.dot(self.H, container_b)))

        rgb = mul_rh + "0000", mul_gh + "0000", mul_bh + "0000"

        return self._bin_to_int(rgb)

    def merge(self, image1, image2):
        """Объединие изображения 2 с изображением 1.

        :param image1: первая картинка
        :param image2: вторая картинка
        :return: Новая объединенная картинка.
        """
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        i_sm = 0
        j_sm = 0
        for i in range(image1.size[0]):
            for j in range(0, image1.size[1] - 4, 4):
                is_valid = lambda: i_sm < image2.size[0] and j_sm < image2.size[1]
                rgb1 = map1[i, j]
                rgb2 = map1[i, j + 1]
                rgb3 = map1[i, j + 2]
                rgb4 = map1[i, j + 3]
                rgb_sm = map2[i_sm, j_sm] if is_valid() else self.BLACK_PIXEL
                rgb_arr = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb_sm)
                new_map[i, j] = rgb_arr[0]
                new_map[i, j + 1] = rgb_arr[1]
                new_map[i, j + 2] = rgb_arr[2]
                new_map[i, j + 3] = rgb_arr[3]
                j_sm += 1
            j_sm = 0
            i_sm += 1

        return new_image

    def unmerge(self, image):
        """Раскодировать картинку.

        :param image: Входное изображение.
        :return: Раскодированная картинка.
        """
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        i_sm = 0
        j_sm = 0
        for i in range(image.size[0]):
            for j in range(0, image.size[1] - 4, 4):
                new_map[i_sm, j_sm] = self._unmerge_rgb(pixel_map[i, j], pixel_map[i, j + 1],
                                                  pixel_map[i, j + 2],
                                                  pixel_map[i, j + 3])
                j_sm += 1
            i_sm += 1
            j_sm = 0

        return new_image


def main():
    parser = argparse.ArgumentParser(description='Steganography')
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge')
    merge.add_argument('--image1', required=True, help='Image1 path')
    merge.add_argument('--image2', required=True, help='Image2 path')
    merge.add_argument('--output', required=True, help='Output path')

    unmerge = subparser.add_parser('unmerge')
    unmerge.add_argument('--image', required=True, help='Image path')
    unmerge.add_argument('--output', required=True, help='Output path')

    args = parser.parse_args()

    if args.command == 'merge':
        image1 = Image.open(args.image1)
        image2 = Image.open(args.image2)
        Steganography().merge(image1, image2).save(args.output)
    elif args.command == 'unmerge':
        image = Image.open(args.image)
        Steganography().unmerge(image).save(args.output)


if __name__ == '__main__':
    main()
