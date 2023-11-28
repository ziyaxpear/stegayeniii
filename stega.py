try:
    from distutils.command.install_egg_info import safe_name
    import streamlit.components.v1 as components
    import json
    import os
    from io import BytesIO
    from PIL import Image
    import streamlit as st
    import numpy as np
    import base64
    import json
    import os
    import ipfshttpclient


except Exception as e:
    print(e)
# PIL : açık kaynak kodlu grafik işleme kütüphanesidir. Bu kütüphane,
# içinde barındırdığı hazır fonksiyonlar sayesinde programcıya üstün bir grafik işleme imkânı sunar.
# Birçok grafik türünü açıp kaydetme yeteneği ile birlikte çizim, düzenleme,
# filtreleme gibi işlemlerde kullanılabilecek fonksiyonlara sahiptir.
# lsb en önemsiz bit   \\least important bit
##############################################3
# io : Senkron ve asenkron olmak üzere iki tür I/O işlemi bulunmaktadır.
# Senkron I/O işlemlerinde uygulama bloklanmakta yani I/O işlemi tamamlanana kadar beklenilmektedir.
# Asenkron I/O işlemlerinde ise olayın tamamlanması beklenmez,
# uygulama bloklanmaksızın bu süreç boyunca başka işlemler yapılabilir
# buradaki işlevi vewrilen dosyaları türleri ile açmak örnek f= open("myfile.jpg","r",encoding,"utf-8") gibi bir
# planmlama çalıştırma için bu kütüphane kulannıldı
STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
astyle = """
display: inline;
width: 200px;
height: 40px;
background: #F63366;
padding: 9px;
margin: 8px;
text-align: center;
vertical-align: center;
border-radius: 5px;
color: black;
line-height: 25px;
text-decoration: none;
"""
st.set_page_config(
    page_title="Steganografi Bilimine Yeni Bir Boyut",)
# Bazı Faydalı fonksiyonlar ============================
# iki görüntü arasındaki 'Ortalama Kare Hatası', iki görüntü arasındaki kare farkının toplamıdır;
# NOT: iki resim aynı boyuta sahip olmalıdır
# asytpe: veri analizinde kullanılan bir işlemdir asynic kütüphanesinden çekilir.
# shape :bir numphy fonksiyonudur ve eleman ekleme işi yapar
tabs = ["Steganografi", "Blokzinciri ","Hakkında"]
page = st.sidebar.radio("Sekmeler", tabs)
image1 = Image.open("mona3.png")
image3 = Image.open("tablet.png")
image4 = Image.open("kalem.png")
image5 = Image.open("kripto.png")
image6 = Image.open("neden blok zinciri.png")
image8 = Image.open("meta.png")
image9 = Image.open("650x344-python-nedir-egitim-dersleri-nereden-alinir-phyton-ile-neler-yapilabilir-tk1-1600422751598.jpg")
image10 = Image.open("download.jpg")
image11=Image.open("kafa.png")
image12=Image.open("s.png")
image13=Image.open("b.png")
image14=Image.open("blokzinciri.png")
video_file = open('Steganografi Nedir.mp4', 'rb')
video_bytes = video_file.read()
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # MSE'yi döndürün, hata ne kadar düşükse, iki görüntü o kadar "benzer" olur
    return err
# BytesIO: Değişkenlerle yaptığımız gibi, io modülünün Byte IO işlemlerini kullandığımızda
# veriler bir bellek içi arabellekte bayt olarak tutulabilir.
def upload_to_ipfs(image):
    try:
        # Connect to an IPFS gateway (you can use your own IPFS node)
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

        # Upload the image to IPFS
        res = client.add(image)
        ipfs_hash = res['Hash']

        return ipfs_hash

    except Exception as e:
        st.error(f"Error uploading to IPFS: {str(e)}")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_image:
    ipfs_hash = upload_to_ipfs(uploaded_image)
    st.image(uploaded_image, caption=f"IPFS Hash: {ipfs_hash}")
def get_image_download_link(filename, img):
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = '<a href="data:file/png;base64,' + img_str + '" indir=' + filename + ".png" + ' style="' + astyle + '" target="_blank">Resmi indir</a>'
    return href
#  dump . bir değer döndürmez ama verilen değeri istenilen konuma gönderir
def get_key_download_link(filename, key):
    buffered = BytesIO()
    key.dump(buffered)
    key_str = base64.b64encode(buffered.getvalue()).decode()
    href = '<a href="data:file/pkl;base64,' + key_str + '" download=' + filename + ' style="' + astyle + '" target="_blank">Download Key</a>'
    return href
# Algo 1 =======================================
# Pikseller, 8 bitlik ikili verilere göre değiştirilir ve sonunda döndürülür.
def modPix(pix, data):
    datalist = [format(ord(i), '08b') for i in data]
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        # Bir seferde 3 piksel çıkarma
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        # Piksel değeri 1 için tek yapılmalı ve 0 için bile, pix bir pikselin bir kanalıdır
        for j in range(0, 8):
            if (datalist[i][j] == '0'):
                pix[j] &= ~(1 << 0)
            elif (datalist[i][j] == '1'):
                pix[j] |= (1 << 0)
        # Her kümenin sekizinci pikseli, daha fazla okumayı durdurup durdurmayacağını söyler.
        # 0, okumaya devam et anlamına gelir; 1 mesajın bittiği anlamına gelir.
        if (i == lendata - 1):
            pix[-1] |= (1 << 0)
        else:
            pix[-1] &= ~(1 << 0)
        # yield : iteratyrler ile beraber çalışır aynı mantıkla döngülerde tekrarrı sağlar
        pix = tuple(pix)
        yield pix[0:3]  # pixel 1
        yield pix[3:6]  # pixel 2
        yield pix[6:9]  # pixel 3
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        # Değiştirilmiş pikselleri yeni görüntüye yerleştirme
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
# Verileri görüntüye kodlayın
def encode(filename, image, bytes):
    global c1, c2
    data = c1.text_area("Kodlanacak veriyi giriniz", max_chars=bytes)
    if (c1.button('Encode', key="1")):
        if (len(data) == 0):
            c1.error("Veri boş")
        else:
            c2.markdown('#')
            result = "Verilen veriler, verilen kapak resminde kodlanmıştır."
            c2.success(result)
            c2.markdown('####')
            c2.markdown("#### Kodlanmış resim")
            c2.markdown('######')
            newimg = image.copy()
            encode_enc(newimg, data)
            c2.image(newimg, channels="BGR")
            filename = 'encoded_' + filename
            image_np = np.array(image)
            newimg_np = np.array(newimg)
            MSE = mse(image_np, newimg_np)
            msg = "MSE: " + str(MSE)
            c2.warning(msg)
            c2.markdown("#")
            c2.markdown(get_image_download_link(filename, newimg), unsafe_allow_html=True)
# Görüntüdeki verilerin kodunu çözün
def decode(image):
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        # ikili veri dizisi
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
# sidebar. yazılmak iistenen değer ve fonksiyonları streamlite de yan tarafa yazar ,
# md . de kullanılan href monalisa resmine ulaşır
def main():
    global c1, c2, d1, d2

    if page == "Steganografi":
        st.markdown("<h1 style='text-align:center;'> Steganografi Hakkında Kısa bir Tarih</h1>", unsafe_allow_html=True)
        st.image(image1, width=700, caption="Steganografi Nedir?")
        st.markdown("[Steganografi](https://bilgisayarkavramlari.com/2009/06/05/steganografi-ve-lsb/), mesajı gömme yoluyla bilgiyi saklama sanatı ve bilimidir. Bu yaklaşım, bir nesnenin içerisine bir verinin gizlenmesi olarak da tanımlanabilir. Bu yaklaşımla ses, resim, video görüntüleri üzerine veri saklanabilir. Görüntü dosyaları içerisine saklanacak veriler metin dosyası olabileceği gibi herhangi bir görüntü içerisine gizlenmiş başka bir görüntü dosyası da olabilir. Steganografinin birinci amaç, bir mesajın varlığını saklamak ve bir örtülü kanal yaratmaktır. İkinci amacı, mesajın içeriğini saklamak olan kriptolojinin bir parçası olarak görmektir. Bu iki tekniği beraber kullanmakta mümkündür. Fakat steganografi ile kriptografi aynı işlevi görmez. Kriptografide gizlenen içeriğin şifrelendiği bellidir ve bu yüzden şifrelendiği apaçık belli olabilir. Steganografide saklanan veri belli olmadığından bilginin istenilen kaynaklara ulaşması daha güvenli bir hal alır.  Bunun için gizli mesaj önce encrypt (şifrelenir) edilir, sonra steganografik yöntemlerle dijital bir verinin içerisine saklanabilir.")
        st.image(image12, caption="Steganografi")
        st.markdown("Steganografi kelimesi Yunanca “steganos: gizli, saklı” ve “grafi: çizim ya da yazım” kelimelerinden gelmektedir. Yunanca bir kelime olan steganografinin tam karşılığı olarak “covered writing (kaplanmış yazı)” diyebiliriz. Steganografi, Antik Yunan zamanına kadar uzanan oldukça eski bir veri gizleme yöntemidir ve bugün kullanılan pek çok orijinal özelliği antik Yunan medeniyetinden gelmektedir. Sparta ve Xerxes arasındaki savaş esnasında, Dermetaus Xerxes’in işgal için beklemede olduğunu Sparta’ya haber etmek istedi. Bunun yapabilmek içinde, tahta tabletlerin üzerine mesajını yazarak bunları balmumu ile kapladı. Balmumu ile kaplı olan tahtalardan hiçbir şey gözükmediği içinde, nöbetçiler hiç kuşkulanmadı. Bundan sonraki zamanlarda da özellikle savaşlarda bu steganografi tekniğinden oldukça yaralanılmıştır.")
        bir_kac_hikaye = st.selectbox("Aşağıda Steganografi hakkında birkaç hikaye örneği verilmiştir. İstediğinizi okuyabilirsiniz. ",("Birkaç Hikaye","Heredot'un Hikayesi", "Bal Mumu Hikayesi", "Mor Ötesi Işınlar", "Günümüzde Steganografi"))
        if bir_kac_hikaye=="":
            st.write("Birkaç hikaye")
        elif bir_kac_hikaye == "Heredot'un Hikayesi":
            st.image(image11, caption="Köledeki Steganografi")
            st.write("Herodot’un bir hikayesine göre Pers saldırısının öncesinde saçları tıraşlanan bir kölenin kafasına yazılan uyarı mesajı, saçlarının uzaması sayesinde saklanmıştır. Bu sayede, mesaj dikkat çekmeden gerekli yere ulaşabilmiş, ulaştığında da kölenin saçları tekrar kesilerek uyarı okunabilmiştir.")
        elif bir_kac_hikaye == "Bal Mumu Hikayesi":
            st.write( "Eski Yunanistan’da, insanlar mesajları tahtaya yazıp üzerini mumla kaplarlardı. Böylece cisim kullanılmamış bir tablete benzerdi öte yandan mumun eritilmesiyle birlikte içindeki gizli mesaj okunabilirdi.")
            st.image(image3)
        elif bir_kac_hikaye == "Mor Ötesi Işınlar":
            st.write( "Özellikle 1960’larda mor ötesi boya ile yazı yazabilen sprey ve kalemler modaydı. Bu kalemlerin yazdığı yazılar, sadece bir mor ötesi ışıkla görülebiliyordu.")
            st.image(image4)
        elif bir_kac_hikaye ==  "Günümüzde Steganografi" :
            st.write("Günümüz Dijital Dünyasında artık bir mesajı saklamak istediğimizde ya da bir dosyamızı gizlemek istediğimizde ilkel yöntemlerden ziyade dijital yöntemler kullanılabilir. Bu projede Python programlama dili yardımı ile bir veriyi kolaylıkla saklayabiliriz.")
            st.image(image5, caption="Dijital Steganografi")
    elif page == "Blokzinciri ":
        st.markdown("<h1 style='text-align:center;'> Blokzinciri</h1>", unsafe_allow_html=True)
        st.image(image6,caption="Blokzinciri")
        st.markdown("""[Blokzinciri](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2849251) 2008 yılında ortaya atılmış, 2009 yılında ise Bitcoin sanal para birimi ile birlikte tanınmaya başlamıştır.Bu teknoloji dağıtılmış bir kayıt defteri olarak tanımlanmaktadır. Daha kapsamlı bir ifadeyle Blokzinciri, dağıtık, paylaşılan, şifrelenmiş, geri dönüşü olmayan ve bozulmayan bir bilgi deposudur. Blokzinciri, ağ yardımı ile sistemi kullanan kullanıcılar arasındaki işlemlerin tümünü doğrulayarak saklayan bir sistemdir. Bu yüzden bütünlüğüne güvenilir bloklar ve bu blokları oluşturan sorgulanabilir işlemlerden oluşan bir veritabanı olarak tanımlanmaktadır.""")
        st.image(image13,caption="Blokzinciri")
        st.markdown("""[Blokzinciri](https://dergipark.org.tr/en/download/article-file/1081395) sisteminde işlemler bloklar halinde tutulur ve bu bloklar birbirine bağlanarak zincir oluşturulur. Belli kurallar çerçevesinde oluşturulan bloklar sisteme yazılmaktadır. Daha sonra blok tüm dağıtık kayıt defterlerine yayılır ve eklenir. Yeni blok oluşturmada bir önceki bloğa ait özet alınır ve ikinci blok üretilerek zincire ekleme yapılmaktadır. Bu yapı tüm blokları birbirine bağlayan ve bir önceki bloğun özeti ile beraber olacak biçimde devam eden bir yapı ile sürdürülür. Bir işlem gerçekleştiğinde mevcut ağ üzerinden yayınlanır ve şifreleme algoritmaları ile bu işlem doğrulanarak blok oluşturulur. Sisteme dahil olan her düğüm, sistemdeki herhangi iki kişi tarafından yapılan bu işlemi onaylayarak kaydını tutar. Bu sayede blok doğrulanır, sonrasında bu bilgi asla değiştirilemez veya silinemez. Her blok birbirine zincirlenerek eklenmeye devam eder. Böylece başka biri onları hiçbir zaman değiştiremez.""")
        st.image(image14, caption="Bloklar")
        st.markdown("""Sistemde bulunan her bir kullanıcı bir düğümü ifade eder. Sisteme katılan her düğüm, kendi başına bir blokzinciri kopyasına yan kayıt defterine bir başka deyişle veritabanına sahiptir. Bu defter bir uçtan uca protokolü kullanılarak diğer düğümlerle senkronize edilir. Bu sayede aracı ortadan kaldırılmakta ve merkezi bir otorite zorunluluğu da gerekmemektedir. Bir düğüm başarısız olur veya işlevini durdurursa, kalan düğümler arızalı yerin yokluğunda tüm işlem ayrıntılarını muhafaza eder. Bu şekilde sistem gerçek zamanlı bilgi sağlamakta ve işlemlerin hata ya da başarısızlık oranlarını azaltmaktadır. """)

    elif page == "Hakkında":
        st.markdown("<h1 style='text-align:center;'> Geliştirilen Proje</h1>",unsafe_allow_html=True)
        st.write("Geliştirlen bu web arayüzü her hangi bir ticari amaç gütmeksizin tamamı ile ücretsiz ve eğitim amaçlı kurulmuştur.")
        st.video(video_bytes)
        if st.checkbox("Projede Kullanılan Programlama Dili "):
            st.image(image9, caption="Python")
            st.markdown("<a href='https://www.python.org/'>Python</a>", unsafe_allow_html=True)
        elif st.checkbox("Projede Kullanılan Editör"):
            st.image(image10, "Pycharm")
            st.markdown("<a href='https://www.jetbrains.com/pycharm/'>Pycharm</a>", unsafe_allow_html=True)
        elif st.checkbox("Resim Gizleme ve Gizli Resmi Çözme"):
            st.sidebar.title("Dijital Görüntü İşleme Projesi")
            md = ("")
            st.sidebar.markdown(md, unsafe_allow_html=True)
            info = """
                                # Resim Steganografisi
                                Steganografi, nesnenin içinde saklı hiçbir bilgi yokmuş gibi izleyiciyi aldatacak şekilde nesnelerin içindeki 
                                bilgileri gizleme çalışması ve uygulamasıdır. 
                                Sadece hedeflenen alıcının görebilmesi için bilgileri açık bir şekilde gizler. """
            fileTypes = ["png", "jpg"]
            fileTypes1 = ["pkl"]
            choice = st.radio('Seçim', ["Encode", "Decode"])
            if (choice == "Encode"):
                c1, c2 = st.columns(2)
                file = c1.file_uploader("Kapak Resmini Yükle", type=fileTypes, key="fu1")
                show_file = c1.empty()
                if not file:
                    show_file.info("Lütfen bir dosya türü yükleyin: " + ", ".join(["png", "jpg"]))
                    return
                im = Image.open(BytesIO(file.read()))
                filename = file.basename("dosya yolu")
                w, h = im.size
                bytes = (w * h) // 3
                c1.info("maksimum veri: " + str(bytes) + " Bytes")
                encode(filename, im, bytes)
                content = file.getvalue()
                if isinstance(file, BytesIO):
                    show_file.image(file)
                file.close()
            elif (choice == "Decode"):
                file = st.file_uploader("Kodlanmış Resmi Yükle", type=fileTypes, key="fu2")
                show_file = st.empty()
                if not file:
                    show_file.info("Lütfen bir dosya türü yükleyin: " + ", ".join(["png", "jpg"]))
                    return
                im = Image.open(BytesIO(file.read()))
                data = decode(im)
                if (st.button('Decode', key="4")):
                    st.subheader("kodu çözülmüş metin")
                    st.write(data)
                content = file.getvalue()
                if isinstance(file, BytesIO):
                    show_file.image(file)
                file.close()
        elif st.checkbox("Örnek Çalışmalar"):
            pass

if __name__ == "__main__":
    main()
