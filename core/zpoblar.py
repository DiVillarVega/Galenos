import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='ggarrido',
        tipo='Cliente', 
        nombre='Gonzalo', 
        apellido='Garrido', 
        correo=test_user_email if test_user_email else 'ggarrido@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='21.722.181-1',	
        direccion='Chorrillo 1885, Rancagua, \nRancagua 40301 \nChile', 
        subscrito=True, 
        imagen='perfiles/ggarrido.jpg')

    crear_usuario(
        username='castorga',
        tipo='Cliente', 
        nombre='Camila', 
        apellido='Astorga', 
        correo=test_user_email if test_user_email else 'castorga@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='20.881.159-2', 
        direccion='San José, Villa Alemana, \nValparaíso 50401 \nChile', 
        subscrito=True, 
        imagen='perfiles/castorga.jpg')

    crear_usuario(
        username='mcaceres',
        tipo='Cliente', 
        nombre='Mauricio', 
        apellido='Cáceres', 
        correo=test_user_email if test_user_email else 'mcaceres@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.066.692-4', 
        direccion='Calle F 304 J Goulart, \nLa Granja, Región Metropolitana \nChile', 
        subscrito=False, 
        imagen='perfiles/mcaceres.jpg')

    crear_usuario(
        username='arodriguez',
        tipo='Cliente', 
        nombre='Alejandra', 
        apellido='Rodriguez', 
        correo=test_user_email if test_user_email else 'arodriguez@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.845.980-4', 
        direccion='Condominio Algarrobal 2 Parcela V- 57, \nChicureo, Región Metropolitana 58118 \nChile', 
        subscrito=False, 
        imagen='perfiles/arodriguez.jpg')

    crear_usuario(
        username='ggarmendia',
        tipo='Administrador', 
        nombre='Germán', 
        apellido='Garmendia', 
        correo=test_user_email if test_user_email else 'ggarmendia@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.332.042-4	', 
        direccion='Chorrillo 1885, Rancagua, \nRancagua 20391 \nChile', 
        subscrito=False, 
        imagen='perfiles/ggarmendia.jpg')
    
    crear_usuario(
        username='mbeltrami',
        tipo='Administrador', 
        nombre='Mia', 
        apellido='Beltrami', 
        correo=test_user_email if test_user_email else 'mbeltrami@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='23.033.054-9', 
        direccion='Los Cerezos 255, Ñuñoa \nRegión Metropolitana 21920 \nChile', 
        subscrito=False, 
        imagen='perfiles/mbeltrami.jpg')

    crear_usuario(
        username='gboric',
        tipo='Superusuario',
        nombre='Gabriel',
        apellido='Boric',
        correo=test_user_email if test_user_email else 'gboric@duocuc.cl',
        es_superusuario=True,
        es_staff=True,
        rut='16.163.631-2',
        direccion='	21 De Mayo 2144, Punta Arenas, \nMagallanes 90231 \nChile',
        subscrito=False,
        imagen='perfiles/gboric.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'BordeLands 3',
            'descripcion': 'Borderlands 3​ es un videojuego de disparos en primera persona con elementos de rol, se trata de la secuela del videojuego de 2012, Borderlands 2. Fue desarrollado por Gearbox Software y distribuido por 2K Games para las plataformas Google Stadia, Microsoft Windows, PlayStation 4, Xbox One, Pc Y Nintendo Switch.',
            'precio': 24990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 10,
            'imagen': 'productos/bordelands3.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Dark Souls II',
            'descripcion': 'Dark Souls II es un juego de rol de acción de 2014 desarrollado por FromSoftware y publicado por Bandai Namco Entertainment. Fue lanzado para PC, PlayStation 3 y Xbox 360. Teniendo lugar en el reino de Drangleic, el juego presenta una jugabilidad de jugador contra entorno (PvE) y jugador contra jugador (PvP). Dark Souls II fue lanzado en marzo de 2014 después de algunos retrasos iniciales, y la versión de PC fue lanzada el mes siguiente.',
            'precio': 49990,
            'descuento_subscriptor': 15,
            'descuento_oferta': 5,
            'imagen': 'productos/Dark_Souls_II_portada.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Dark Souls III',
            'descripcion': 'Dark Souls III es un juego de rol de acción de 2016 desarrollado por FromSoftware y publicado por Bandai Namco Entertainment para PlayStation 4, Xbox One y PC. Tercera y última entrega de la saga Dark Souls, se juega en una perspectiva en tercera persona, y los jugadores tienen acceso a varias armas, armaduras, magia y consumibles que pueden usar para luchar contra sus enemigos. Hidetaka Miyazaki, el creador de la saga, volvió para dirigir el juego tras dejar las tareas de desarrollo de Dark Souls II en manos de otros.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/darksouls3.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Call of Duty: Modern Warfare III',
            'descripcion': 'Call of Duty: Modern Warfare 3 (abreviado oficialmente como Call of Duty: MW3 o Modern Warfare 3) es un videojuego de disparos en primera persona desarrollado por Infinity Ward y Sledgehammer Games, con el trabajo adicional de Raven Software, y distribuido por Activision',
            'precio': 39990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 5,
            'imagen': 'productos/modernwarfare3.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Monster Hunter: World',
            'descripcion': 'Monster Hunter: World es la penúltima entrega de la Saga Monster Hunter, fue anunciado el 12 de junio de 2017, y salió el 26 de enero de 2018 para PS4 y XB1, mientras que la versión para PC salió en agosto de 2018. El juego supone una completa remodelación de la saga. Su expansión, Iceborne, fue anunciada en 2019.',
            'precio': 15990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 20,
            'imagen': 'productos/monsterhunterworld.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Ready or Not',
            'descripcion': 'Ready or Not, a cargo de Void Interactive para PC, es un título de acción táctica FPS que nos pone al frente de un equipo SWAT en el que Estados Unidos está sumido en el caos por violentas bandas criminales. Ofrece total libertad para encarar las misiones, así como una gran variedad de armas y gadgets.',
            'precio': 19990,
            'descuento_subscriptor': 0,
            'descuento_oferta': 15,
            'imagen': 'productos/readyornot.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil 4',
            'descripcion': 'Resident Evil 4 es un juego de terror y supervivencia en el que los jugadores deben sobrevivir a situaciones de miedo extremo. Si bien estos puntos de horror aparecen por todo el juego, se equilibran con los elementos de acción, creando una experiencia de juego impresionantemente variada.',
            'precio': 69990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 5,
            'imagen': 'productos/residentevil4.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sekiro: Shadows Die Twice',
            'descripcion': 'Sekiro: Shadows Die Twice es un videojuego de acción-aventura desarrollado por FromSoftware y publicado por Activision. Dirigido por Hidetaka Miyazaki; se estrenó el 22 de marzo de 2019 para PlayStation 4, Xbox One y Microsoft Windows. Su historia la protagoniza un shinobi llamado Sekiro durante el periodo Sengoku, cuya intención es la de vengarse de un samurái que le atacó y secuestró a su señor.',
            'precio': 59990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 15,
            'imagen': 'productos/Sekiroshadowstwice.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Fallout 4',
            'descripcion': 'Fallout 4 es un videojuego de rol de acción de disparos en primera y tercera persona desarrollado por Bethesda Game Studios y distribuido por Bethesda Softworks. Es el cuarto juego principal de la serie Fallout y fue lanzado en todo el mundo el 10 de noviembre de 2015, para PlayStation 4, Windows y Xbox One.',
            'precio': 25990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 0,
            'imagen': 'productos/fallout4.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy: es un juego de rol inmersivo en mundo abierto que se inspira de los libros de la saga Harry Potter. Disfruta del Hogwarts del siglo XIX. Tu personaje es un alumno o alumna del famoso colegio que tiene la clave de un antiguo secreto que amenaza con destruir el mundo mágico.',
            'precio': 35990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/hogwartslegacy.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Lies of P',
            'descripcion': 'Un juego souls-like de fantasía oscura inspirado en la clásica historia de Pinocho. Este macabro juego souls-like se inspira en una historia que parece incompatible: Las aventuras de Pinocho. En esta sombría reinvención del querido cuento de Carlo Collodi, Pinocho está tratando de encontrar al misterioso Geppetto.',
            'precio': 29990,
            'descuento_subscriptor': 10,
            'descuento_oferta': 10,
            'imagen': 'productos/liesofp.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sea of Thieves',
            'descripcion': 'Sea of Thieves es un videojuego de acción-aventura en primera persona desarrollado por Rare y distribuido por Microsoft Studios para Microsoft Windows y Xbox One. El juego se lanzó el 20 de marzo de 2018 y es un juego de mundo abierto en el que los jugadores asumen el papel de piratas que navegan por el mar abierto y buscan tesoros en islas deshabitadas.',
            'precio': 20990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/Sea_of_thieves_cover_art.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'ArmA III',
            'descripcion': 'Es un videojuego de simulación militar desarrollado y publicado por Bohemia Interactive. Lanzado en 2013, es el tercer juego de la serie ArmA, conocido por su realismo extremo, vastos entornos abiertos y una profunda integración de la táctica militar en el gameplay.',
            'precio': 15990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/arma3.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Europa Universalis IV',
            'descripcion': 'Europa Universalis IV es un juego de estrategia en tiempo real y por turnos desarrollado por Paradox Development Studio y publicado por Paradox Interactive. El juego se lanzó en 2013 y es la cuarta entrega de la serie Europa Universalis. Los jugadores pueden elegir una nación y guiarla a través de la historia, desde el siglo XV hasta el siglo XIX.',
            'precio': 10990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/europauniversalisIV.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Total War: Warhammer III',
            'descripcion': 'Total War: Warhammer III es un juego de estrategia en tiempo real y por turnos ambientado en el mundo de fantasía de Warhammer. El juego presenta cuatro razas jugables: Kislev, Cathay, Khorne y Nurgle, cada una con sus propias unidades, mecánicas y objetivos de campaña. Los jugadores pueden liderar a sus ejércitos en batallas masivas en tiempo real y gestionar sus imperios en un mapa de campaña por turnos.',
            'precio': 10990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/warhammer.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Total War: Pharaoh',
            'descripcion': 'Es un videojuego de estrategia por turnos en tiempo real desarrollado por Creative Assembly Sofia y publicado por Sega . Como parte de la serie Total War , Pharaoh está ambientada en el Nuevo Reino de Egipto y sus alrededores antes del colapso de la Edad del Bronce Final.',
            'precio': 23990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/totalwarpharaoh.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Dragon Ball Xenoverse 2',
            'descripcion': 'Dragon Ball Xenoverse 2 es un juego de rol de acción de 2016 desarrollado por Dimps y publicado por Bandai Namco Entertainment. Es la secuela de Dragon Ball Xenoverse y fue lanzado para PlayStation 4, Xbox One y PC. El juego se desarrolla en un mundo de Dragon Ball en el que los jugadores pueden crear su propio personaje y luchar contra enemigos de la serie.',
            'precio': 5990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/dragonballxenoverse2.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Final Fantasy XVI',
            'descripcion': 'Final Fantasy XVI es un juego de rol de acción de 2023 desarrollado y publicado por Square Enix. Es la decimosexta entrega principal de la serie Final Fantasy y fue lanzado en junio de 2023. El juego se desarrolla en un mundo de fantasía llamado Valisthea, donde los jugadores asumen el papel de Clive Rosfield, el Caballero de las Rosas.',
            'precio': 40990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/finalfantasyxvi.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'New World',
            'descripcion': 'Explora un electrizante videojuego MMO de mundo abierto. Tras un naufragio, llegarás a las costas de la sobrenatural isla de Aeternum, donde vivirás peligros y oportunidades, y te forjarás un nuevo destino. Gozarás de infinitas oportunidades para la lucha, la caza y la forja en medio de la naturaleza y ruinas de la isla. Canaliza fuerzas sobrenaturales o blande armas mortales en un sistema de combate sin clases y en tiempo real. Entra a la batalla solo, con un pequeño equipo o como miembro de un enorme ejército en las batallas JcE y JcJ. La decisión es tuya.',
            'precio': 14990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/newworld.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Elder Scrolls Online',
            'descripcion': 'Es un juego de rol multijugador masivo en línea (MMORPG) ambientado en Tamriel, la antigua tierra que incluye las provincias de Páramo del Martillo, Cyrodiil, Morrowind, Roca Alta, Ciénaga Negra, Bosque Valen, Isla Estivalia, Elsweyr y Skyrim. El juego tiene lugar 1.000 años antes de los acontecimientos de The Elder Scrolls V: Skyrim, a mediados de la Segunda Era. Embárcate en una aventura épica para salvar la tierra de un mal aparentemente imparable en una historia extensa que se puede experimentar por cuenta propia o con amigos.',
            'precio': 20990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/theelderscrollsonline.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['12.845.980-4', '12.066.692-4']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

