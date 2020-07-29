PGDMP     5    +                x            Virtual_department    10.13    10.13 2    
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    16385    Virtual_department    DATABASE     �   CREATE DATABASE "Virtual_department" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
 $   DROP DATABASE "Virtual_department";
             postgres    false                       0    0    DATABASE "Virtual_department"    COMMENT     �   COMMENT ON DATABASE "Virtual_department" IS 'Здесь располагаются все стенды и их основные параметры';
                  postgres    false    2829                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false                       0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16407    comments    TABLE     �   CREATE TABLE public.comments (
    date date NOT NULL,
    author text NOT NULL,
    commentary text NOT NULL,
    serial_number text NOT NULL,
    comment_id integer NOT NULL,
    "time" reltime,
    alarms text,
    number_in_departament integer
);
    DROP TABLE public.comments;
       public         postgres    false    3                       0    0    TABLE comments    COMMENT     �   COMMENT ON TABLE public.comments IS 'В данной таблице будут записываться комментарии по работе со стендами';
            public       postgres    false    197                       0    0    COLUMN comments.author    COMMENT     Q   COMMENT ON COLUMN public.comments.author IS 'Автор комментария';
            public       postgres    false    197                       0    0    COLUMN comments.commentary    COMMENT     J   COMMENT ON COLUMN public.comments.commentary IS 'комментарии';
            public       postgres    false    197                       0    0    COLUMN comments.serial_number    COMMENT     s   COMMENT ON COLUMN public.comments.serial_number IS 'Серийный номер установки, стенда';
            public       postgres    false    197                       0    0    COLUMN comments.alarms    COMMENT     �   COMMENT ON COLUMN public.comments.alarms IS 'в данном поле устанавливается текущее состояние стенда: работает, не работает, есть недостатки в работе';
            public       postgres    false    197            �            1259    16413    comments_comment_id_seq    SEQUENCE     �   ALTER TABLE public.comments ALTER COLUMN comment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.comments_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 123123
    CACHE 1
);
            public       postgres    false    3    197            �            1259    16463 
   complaints    TABLE     �   CREATE TABLE public.complaints (
    complaint text,
    user_name text,
    date date,
    "time" reltime,
    urgent text,
    number integer NOT NULL
);
    DROP TABLE public.complaints;
       public         postgres    false    3                       0    0    TABLE complaints    COMMENT     r   COMMENT ON TABLE public.complaints IS 'Здесь будут жалобы регулировщиков и пр.';
            public       postgres    false    200            �            1259    16386    installations    TABLE     B  CREATE TABLE public.installations (
    serial_number text NOT NULL,
    model text NOT NULL,
    phases text NOT NULL,
    to_date date,
    poverka_date date,
    number_in_departament integer NOT NULL,
    inkotex boolean,
    alarms text,
    calibrovka text,
    poverka text,
    installation_id integer NOT NULL
);
 !   DROP TABLE public.installations;
       public         postgres    false    3                       0    0    TABLE installations    COMMENT     �   COMMENT ON TABLE public.installations IS 'Здесь содержатся все установки и их основные параметры';
            public       postgres    false    196                       0    0 "   COLUMN installations.serial_number    COMMENT     l   COMMENT ON COLUMN public.installations.serial_number IS 'Серийные номера установок';
            public       postgres    false    196                       0    0    COLUMN installations.model    COMMENT     S   COMMENT ON COLUMN public.installations.model IS 'Модель установки';
            public       postgres    false    196                       0    0    COLUMN installations.phases    COMMENT     c   COMMENT ON COLUMN public.installations.phases IS 'Количество фаз установки';
            public       postgres    false    196                       0    0    COLUMN installations.to_date    COMMENT     �   COMMENT ON COLUMN public.installations.to_date IS 'Дата последнего ТО: проверка работоспособности, чистка, замена изношенных деталей';
            public       postgres    false    196                       0    0 !   COLUMN installations.poverka_date    COMMENT     �   COMMENT ON COLUMN public.installations.poverka_date IS 'Дата последней поверки эталонного  счетчика';
            public       postgres    false    196                       0    0    COLUMN installations.inkotex    COMMENT     u   COMMENT ON COLUMN public.installations.inkotex IS 'Установлена ли доработка инкотекс';
            public       postgres    false    196                       0    0    COLUMN installations.alarms    COMMENT     k   COMMENT ON COLUMN public.installations.alarms IS 'Текущие неисправности стенда';
            public       postgres    false    196                       0    0    COLUMN installations.calibrovka    COMMENT     �   COMMENT ON COLUMN public.installations.calibrovka IS 'Модели счетчиков совместимые с данным стендом';
            public       postgres    false    196                        0    0    COLUMN installations.poverka    COMMENT     �   COMMENT ON COLUMN public.installations.poverka IS 'Модели счетчиков поверяемые на данном стенде';
            public       postgres    false    196            !           0    0    TABLE installations    ACL     4   GRANT ALL ON TABLE public.installations TO "Admin";
            public       postgres    false    196            �            1259    16475 !   installations_installation_id_seq    SEQUENCE     �   ALTER TABLE public.installations ALTER COLUMN installation_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.installations_installation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 121212
    CACHE 1
);
            public       postgres    false    196    3            �            1259    16424    pc    TABLE     �   CREATE TABLE public.pc (
    ip text NOT NULL,
    serial_number text NOT NULL,
    name_pc text NOT NULL,
    radmin text,
    windows text,
    net_monitor text,
    inkotex text,
    other_soft text,
    alarms text
);
    DROP TABLE public.pc;
       public         postgres    false    3            "           0    0    TABLE pc    COMMENT     N   COMMENT ON TABLE public.pc IS 'Данные компьютеров цеха';
            public       postgres    false    199            #           0    0    COLUMN pc.serial_number    COMMENT     �   COMMENT ON COLUMN public.pc.serial_number IS 'серийный номер стенда на котором установлен ПК';
            public       postgres    false    199            $           0    0    COLUMN pc.radmin    COMMENT     Y   COMMENT ON COLUMN public.pc.radmin IS 'установлен радмин или нет';
            public       postgres    false    199            %           0    0    COLUMN pc.windows    COMMENT     F   COMMENT ON COLUMN public.pc.windows IS 'версия виндовс';
            public       postgres    false    199            &           0    0    COLUMN pc.net_monitor    COMMENT     S   COMMENT ON COLUMN public.pc.net_monitor IS 'Установлен ли NetMonitor';
            public       postgres    false    199            '           0    0    COLUMN pc.inkotex    COMMENT     N   COMMENT ON COLUMN public.pc.inkotex IS 'Программы инкотекс';
            public       postgres    false    199            (           0    0    COLUMN pc.other_soft    COMMENT     M   COMMENT ON COLUMN public.pc.other_soft IS 'другие программы';
            public       postgres    false    199            )           0    0    COLUMN pc.alarms    COMMENT     �   COMMENT ON COLUMN public.pc.alarms IS 'Отмечается сосояние компьютера: работает, не работает, есть проблемы';
            public       postgres    false    199                      0    16407    comments 
   TABLE DATA               ~   COPY public.comments (date, author, commentary, serial_number, comment_id, "time", alarms, number_in_departament) FROM stdin;
    public       postgres    false    197   �4                 0    16463 
   complaints 
   TABLE DATA               X   COPY public.complaints (complaint, user_name, date, "time", urgent, number) FROM stdin;
    public       postgres    false    200   �f                 0    16386    installations 
   TABLE DATA               �   COPY public.installations (serial_number, model, phases, to_date, poverka_date, number_in_departament, inkotex, alarms, calibrovka, poverka, installation_id) FROM stdin;
    public       postgres    false    196   �f                 0    16424    pc 
   TABLE DATA               s   COPY public.pc (ip, serial_number, name_pc, radmin, windows, net_monitor, inkotex, other_soft, alarms) FROM stdin;
    public       postgres    false    199   zk       *           0    0    comments_comment_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.comments_comment_id_seq', 184, true);
            public       postgres    false    198            +           0    0 !   installations_installation_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.installations_installation_id_seq', 16, true);
            public       postgres    false    201            �
           2606    16431    pc ID 
   CONSTRAINT     ]   ALTER TABLE ONLY public.pc
    ADD CONSTRAINT "ID" PRIMARY KEY (ip, serial_number, name_pc);
 1   ALTER TABLE ONLY public.pc DROP CONSTRAINT "ID";
       public         postgres    false    199    199    199            �
           2606    16422    comments comment_id 
   CONSTRAINT     v   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comment_id PRIMARY KEY (date, author, commentary, serial_number);
 =   ALTER TABLE ONLY public.comments DROP CONSTRAINT comment_id;
       public         postgres    false    197    197    197    197            �
           2606    16470    complaints complaints_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (number);
 D   ALTER TABLE ONLY public.complaints DROP CONSTRAINT complaints_pkey;
       public         postgres    false    200            �
           2606    16472    installations installation_id 
   CONSTRAINT     }   ALTER TABLE ONLY public.installations
    ADD CONSTRAINT installation_id PRIMARY KEY (serial_number, number_in_departament);
 G   ALTER TABLE ONLY public.installations DROP CONSTRAINT installation_id;
       public         postgres    false    196    196                  x��}[�\ו�s�W�STU:�Խ<3�đbt!H�3��IˤAq2p��lR��
)���H������"������_�/ɺ���.���%�}�s�e�u�ַ�.�2o��v1lT��ZV�ꤚ��fY�u���Ө~X߃�O���:[߭Vլ���W�l}�?9^Z-���B~aJ��G����>|�Eu�~�~��������<~?+��:Y�-� ?v c��N3x>>߂w��8��)|o	�U���������x��^'��ó� �s���ۃ��q�'��3z̼Z�X���[�S�.�4{�ʛ�o�۾|�#�o�;i�0|�����s\��� �y�l����>�y&�
���6���l�������9�`C�geKV��|޲p�O/�U?�A�?_?�����-w��X�{<���x�C��Y���c�����޸Q�F�Or��h��ۿj��?)ϕ����x�U{��).��1L���$m^���x��~�4i�A��%�<A?���d���j��p:��͝;k����FQ�b4�w'���U����ߨ� +r7L���6���+x�:,0K�!N3@L�9��8qx
	Ҋן�?{�oX?���x�C�x�Ni��'�;�W(+��N����Fw�(Ɠ.nU�ڻ�naw�W?:_�֠4�[�k:�q���\�Į2ڙ�N�{�ҋ2�r�>��EZk!X�7�&y�q�뿹}���OE���0��]��x|��x�yR48V�6� ,�:N�����3�A�?����@F	3�t���|��+@�#U0����H�m�T
�ޤ_LzE�TF�|��FyL��o�M�	N;�����p0+:�]P�I1�Ex�Zcp������0�E�k�IٝtǍ���\'!/�[��!�������h���j� q�w��{�+�����
��KV6���`� �c;��
��%���1U�!:.�E_�����5�Ȅ�$��e>��׻��O���G%�!���?LKYc�@����?`Y�SA�Xb�Os�/ǚv���$X�/>�S�Y�"���/��N�E�m������r��U-fUA�%%����#>�ndqaD�d�Y���#+}d܇y��Μ��HgI2�T��y��x͹)�:Y��w)^f�!l��*2#���Y�����I;&s���Ck�����i�a��x]kG��ڡ��C�`1fE��k�V��Hø�ĕ�����Ћ� ~Q'+a��Ez�-܌�M����D<�i�8������ZHuq��݅g���ľ)�Av��wC��2�Li��������U��Ʈi��k��[G��\ ���g,���DS�˂��R���Қ�j��{�da�Ǎ�]+cc�B&�nЧ�q{�iG��C{z:�AG���&�?��~�ў����	^�z7t�tc7��>BY�}惖x��4�@�廸b�`�?����aII�Xr���8���l���n�B^Ј�h�t���G�p'�_���'�� {~�u��xl<�����������@N��O<e�}JFg�vvs8���le���L�oT�s�p��E߀N�J���O�/ld`u�����aE��|����+�G�:S!�=d�\?�DjFgx��|�3�C�էz�ܗZ��=E�x��$cd��J�X&�9"��b��8�l�{��PP8D�Qf	�+˫?����ɡ�,�V�z����?8�ۈ�c�؊�����C� �[����M�J�,�?��޵:7�㕻��tN�u�?��g��U	�'-c�~�'m�=w)(?���gdѦrH@��?�bz��&?C.l�s��\�������3�{Պ|�5v��1/��K}���\Ӌ�$G�u�y���9���ȟ��9.�G��3�&Q��B��G��Ƹ���M�ox$r�;���\��~w��\v�(�g���L��4<!c���eS�?�V�"J�sm�K�#~3��+0����B�0�����{X��.���yW������9D������V~���G���8��U"��E�JA��x\��]��L*#:�QM;//YU��b3AA���P�[7a��%�UvYM0�.	�à�
m����|d�*:��Ȝ�����@�����9�9�kl7GfC��0���^D�Z7)eoB��� ��|�=�R8�`�#P!;W�|��_e���n��Ƿ�q�ZPv�X7�f��y�q%=5P������Z���^�0Z<�1���T�E�>e�%K�ܕ�S�%;����[w�(�I����W�7�6Wb��6���x��~_�I��񮙢�؊{�@�j�Db��Ɓ�R��&��,��q����i����;oK\� ��I-i�m�J�N����S���ҐyI�1����S<#b��ZfR��J���G�Wb ����U�L���-�P,�j��Y�S6QK�x�cuÊ��;�Q���9��G��+��ԟ��^e�;+"O<c�-fMϸD��Nz��h��$�
)2��	c��/o�+̋,c?��t�Ə�q��;�����
_�W_��WQ��W�l�%4����l��E�B3j *�$,�?)Kj���|�X{�]8@��M�7+ƭ2?�g�w[q�>��#ҡ���!����E����"T�1X����E<��۝��=O�Y����5�q�8~;��J�o�J�b���jax�P���]�S}��'���7��!�5�4s��Ĳ,�D���?��Ut��T�5�E19�/صx�A��9���4���1�� �X�ߵ��q��w&t(���N�|+�h�f
����f�������F����3k� �A�e�(o<�4w�
���`N٧Y�v&Av�:����]�YA���8�H� Y�jڔ�L�wΆ��
l�^�*�>��5%�v� K���%�8gl;�D��S�^vy��$���;-��˿U�&JI���}L���r*l����sz5��2t�W�A�.^��4HAwHo<)<�m���F�8>ϳZW����rcq�r�h�N�+��8����	������g=EO^��^�M�w�7�뗯���wW�y=��>�69�B��m�Oz=I���J-P���թ�ڔ�"r�!9���D5�6\E�UX�+�2=�� �0<w�Sҟ3Ǉ%�I�5�� -�-R�{�����𣻒���$�&�7Aڣ�	�#+E�P�K���L	xD�8����%�Ugn���k�dZ�{Ώu=xl+#��(U��\x�]\!��._9W/�@&|H,8f��m�%�y�&E��mV���fcx^�C�҅8ٜVi���6�6-� �`i�<�)� ��]�,��y���`�Q�+��(��q�_ͻx���^8|!@����0�uV���\qՉPB"��x8A˞�3��I��u��u�H-В�@i	����:U�>dۆG���r(��p6t_���G���\���	\�1��?s�kwc���ČF�e���v�p��誧���+�p��������!�T���z��8	��h`��.	eW�͍+b��|Ds=V* a���t�$��nsƞ!R��#�05!�eO��$�-�G�(y��䋳q�CQ�/1n�BaR/�'��L����$vmRN6O�1�	�@	�f����1��`Fg�&�k3,]���^5��Z���ܡ�����=�kj�* >�����9�CE��!�?�>�2'���[��QL�ħ�H~���V�!�D��Ir.�m��4�#V�缏��.<=M�?�c�r����|��r�/+gU�771��'g�O�p׽E%�>��߫#�tӎ��B'u�8򞝇^%�������sA�z����6�@�h.�u��黁���xQ�i}�?���L��&94��(�69T{��,�c��܍;�8a/��x��| @�<�%(��DL�������Խd0��9�q�oo���KMG�:|0��H�Ӧ-��7o}p��+o]�v���o���߾z�څ[7�ܾ�qv�Û}|�    �.e�d����o���?{�9/�dr��=����/���Uy�<�z���ݱy2Wg���7��d�r���H$3b�_0��Fk�e���ɂ��3�ۿ��,X�H���bz��i6B �Y��I��x��k�Pb�qeN�I�Ni0�>ћ�ѩF7 ��Ui޳L(�(;2x�]fU��8,�3ƭ✸�$��u�ȥ�/�������Yf'r�k��z�O2�+!,-��E4f�#�en$�`ha� P J�o�B�����-s�ˀ���#N��1ȱ��ۼ�HzY���-�5��!�DB�W�D���n��5X�a�Q���f��ziy�G�1|-�%i����v�1����f�x��/��Rf�V�c���Ĉȗ�Q$T-��Ax�0(���8��ә���@t�rhR�n�R;���NѯG�n�V
~)J�����ZH�t,%ϡ��VD�yj���|X4㕽I�C ��2���w�!%�Ĥ�G��4%o���'{���fJ�|!KvLu)�TJ��H��=�sg]����SaB�*���m��@W�.h�x�HjIL��M�}qDR5!�c��lzN�°�ܚ)�<م�j�jd����g��sد�YI�v7�Z�b-�������#��mY�JP�dإ�7(=�aDGE8���A�ֳ��R���|�M88TN�6�t
�2oT�(��-6�w"�O�H�_������	x�X�c�T!�)ㄺ.[�xYrn�Y��zFN�R�]|�	
4��b��������c��w�)�����Y�����aMZ�#�NPyU�:�|A5@X`���Л����U��9j���M����D$�e^t�N�T�7+uJʓ'}Ϳ9���h+E�+�W_T�߉&D�� o�H�c��A�0�!��������#&�H�˓c���I������%S�9''r&���3`��8i9
�R_(���,�: \ը5�C
Sϯ4�-���ȉ��E�l�ZE�*��NB9�<L��`/�H��t'S��"�t�]�إć��bYa��£r6�t�dΤ�_��A-�Τ
y�|��RUh,[����_�?�l=����n��]na��O�&G�O����`+���]T�8�W����Δ�SYe�����>W<��C����]�$�CPS��_{�5�Am���TW�`Y�J��))Ψ����ꚮ�Zt��L�z��i����%i�Z�(.@���"�}�ޫ_��\A�A�� TV�n��3g<����he`J�uC�{į�����lHs�p�S�H2�tg�7)-��$��i_�>��b�s�Ɂ��"���"?xDbC?m��=�t�y��e��7�W��/Z�E���_2.�IV��l{�4�&�*����C1&{�R��4 !��0C]�@�@(�p�e�v��/�4)�P�-·-^�_J�9�0�	bǑ�Ny�������U5p������D�J�ͅ[/�+���֪D�Ie2�G^~�#��'��cw K�c��ele���Ͳ�9��.�C�fvU��#xd�K�~L��Lb$9<TC���`XZw�-&������]R)�� Ϧ�I�f��{/��R�Mi�&S�$4�v�� �#��K�7~�cQ:S��*-�f'�MH�������5�^�p#�8U`�e�V�H��´�n��s���i�|�7��V.1��4�r1����;R�$2���b.�b�>��>�-w�O��$EN�-�z���@0א�r�s�I�g�<�)��r��ۊ��� "gw�?19���M�̿��d7�v0��Z��s)�$�J�~tQR��6�&������L��������F�3���ܞ�b)@*d� P��,�I}R؍��Ҍ�&%����w���s�λ���7���kF�\r׺}$Ը�e���%	L�vֶ�v�9L�m6rp�z���{���)t���p^��rr��H��yn{Y�9��?����J��L��f<j�
�@�M�Z�e�TY��g�A�'_���`�[��P�Uj�b��Ln�6�:�o�)XP.v�Aq@fq�M�����^�w:���i�2E�OaV�Vˡ|���G�L8[�:��!�:�-"o娣�Z�q��,
�{��X3�w��[l���!ə�D����"��=��j��_��d�;�dgL%ti�D=[��-�0U�cE=V�M��w���|�iF/(�"�R��}.5�+-��LSL�0R�����U\G��d���J18����9��:(��$* b8]}�U�k(�Z ����R���s:O\ R�˘����_q�q����$Y�B� z�sQՏ�mva�f��z(1V� $k&ю�2<eBQ��u�>m� �mw����4T��5���i\2ь�y��7����g�85��5��el�A�W�s۔�I��l�z���IT�= �a��*��.�f2��o+㲈"p���n��Ć��]$�\���E~����Em[%��?�Yr���� �����F&�=d�R�m0��gXH_�ul ��b9ᕫі�֩�M)�~!h0A��&m� (��r���慸�O�X�Y�S�ImGza	􍸲@�&ɍn�V2c���L~�x��"Ts��X���ͺ,�39�l�y���
�����P��e��FŪ+�Y��O'd^b�̩}�)���~(�"j��
�����rʮ�µ!��J� ���X��]���@���Wڜ�#��:�ض��F���D��LT�a^'t�1���M0�6��,t��tYcS��Y�Ay96��Ud�0,;!⊗kAFȱ������荆o_��ӞG��3��2m�R�/[ʈ��V9%��I���v�1K�m�y_���D�������|�91âQ�.Q�91��A6��IH/3���0N���e~�Y�㔃�������wq������,�J���0�T������+V:_���P�NFw�/Q6�,]���N���/3E�m ��}��;�]�sS �^cXb�����/����:IS��"}AE�y7o{����ʞ�3�l����-Z��6��c}0o��������C<�\f��j��N<Sۦ^Z�~�M��_�A �OBT2E���xݕd�)�Z
}�n�V�gn8@�k_��V֚�o����(Ry�&��CG��(XQ͢tU�,�\$��`r�����m7|5�n�;b����0�KU�$<d�3M	[U?j`�ᄪ��I�����F��A߫C+��"����P
Q�f�h��'�3�V�+�������J�x�Q.´����jL��t��/��ԃ`�n8˻�l�Ȧ�8�Z��C��%�.�uK��d+�,e:QjI��NЅD *(2[��%z���8�N-��~��ô�95KO�6ۡ���Ў�NЛJe�]���NZ�Ɛh%�C�~�	\��i8�g2�vM��j�����J�G
[ВQn�B&�f�Ƣ��:����ǰ����v�����˪�?>�ASK^�uf��֨om�'��['-c)��G"�]1���Fω̬��G6�J*���6(g������#�\��?i[�e|+�l]��6a�������`.\lΨ'*G��o*E���j4��D���aX�����&�Q���&J�a��\e=g�_���{84�����n�_S���/��ds�1�-I�
i�٘>�.̄횂48�MN��خ&Ǫ���XK�ؒ�H��GBRqjh�/�c1�fw�];������$Mªx������u=̢��v�5'���?�R2��!�i'.ޙ���6Z�lL��&��+���ZA��e��G�Fx5����v�A��e�/^��о�yץ�63z"w��+][��o��|��;Y��w�9Ǵq�x2=׵���)]K`�U�����!���u��j���U�=�=����T��h��k��ݞ�B��%z`%��f|�@t֩@���/,h�U?n�����Ǵ�E:{Hf�l���8��^�;wba/�_ߺy�έۻ��YJ�С�������oN�^C�Dy84\�fݪ��:�s�����8E�J�rY�+���d&    M�<P���-b8���<7%�Vǭm��!+ks�!���K��w� �b_Un�U�T����r1OI�YZ�+X�n���茲�o�Wc���}J��kb=(�\߳m-��IE�m�Mp�a���~��f0�̘R4���V�Wm����@����Ts�	�H��"D'���2~�wت��|�����]J����]�n�?��:�.rd��A�����e�"ػ�ƹ�����H�A����_i��x�A,���3�uYC����!��p��~�{�/ӯl�]�oq�ٵǖEY�����ڢ�6]����4�ouoO�\��hӧ*(��=���ӚRb�f��)����m� f2�Ǹ��O���˔cq37岰�ɑz��;�;��nz�z����Pf�֥A^}������\p�(0u��mq~Q��1�,6�R�v&�yOB�oU<�V|C�\���wmR;���J�^ŴYV�.�~�5�I�{ɿw��Ԣ[�W�sT-7�Qx��>�Jp���g����[�a 	�>-�K�:����T�
�A}�A��B��XS"�Y��6��£�S�}�L��*����h����~����e��^iE	Ʀi��<���8$gR��)����Τ���c�յ��z� �[��H�2����_��h���+۳�˵��Va���?H�z����>�p&ל̝z��~�y�IA������#g�wl��.ݶ�c�����~!��bK���]G��!�`�]B�0�5UpԐ�l<h����g��*~�H��J{w,�-�F4q��F"�d5>��MgeI�A��I�Z2��x}�c�����5�_�^S�T�mCt���U`Fl��t-ը�5���?�������W�nM������0-;\���z�A�ʀZMi��0wǽ58|N��?��0��q�.�y�L�{Ԩ��𕽞��h˺t�1J��7�\�J���岾A�����NAx����4����6�,�m����h]�μw�^�=�����߽�n2c��4�6wC|U9�ԸvS���M��S�d̾�p�/��9��'�2������yGԁ�"�X8rC@2��)u<z�>,���6�vI�ҟ�����|���=W���#e|�:9w`P�G}en�
bTֵ��I׼~�YL[kp��:)5�S|�����h�T�,��{�5��X���4��cߊ�D5?���?W�x���[y�|D�Jƭv*�%X�Mn���_X�u�Ȗ��ՔX̉Iv�!���9ㆎ�HR��t$Jk͆�us>,w?�_ZL �r���i�j��s�{�3�O��*i
���=�ÞJC�\TLX�C07��i�[�C���"5/?�__���'��aotnJ!���ߑޑ쓿��T�ÞP�V���S��*?���EFn'a�Kޥһ*�{ѝ.�z�{HDϛb�2]��҈E��g��V�B|�{�ُ��'0�T"���?�q/�Yd�޹~�w:�u�����3 ��,�'�$�tG��e�&�ѣF��L��nj���4Zi#�Y�1y&6��;��P^�l����QUR�n>�n�L�R��e�3�.UbE�:��,�T}o�V,���5z��*y>Z�Β�i�p'
QG+&��#
��b��T1見��Umht�J�n������&��c�U������V-�MQC��87�4"x4	CP{��eG}�-��T�ؖ<��|�L�_�� ���q�h�������hNA�9�Ḧ́�m�-=%/�����i��X��>�wL�e���m�@��v�r��\����-�B�W�H�^�̥j�SڦklԉV�^�Ҧ�A��"j�欹T�9�]L����p����f8Q$M��lA�4y�o�OM�M{�!�z��z����ǰ�焾^$Vɵf�PQ
�n5Bc�D�2/��>��wr� ���Q}$����d]���̣��\�:�0A�����.����@H��U�t_������d�<_��+��;sH5���=�k��AS.����%�=t�ڦÆ��L)��7�=�%��:�\ G�;�n\��[�(Vʭ_;�Q��t���S�b�Ǜ�nC��G�S☠S��;��	��4����n@��UL��M��踻~�d}v�%��z�_U��FK�ƴa$Ӆ<�����s@Q	��=���t��i)1���-O��vP���+H�k÷�r���ލ�cc��Z�4��4eI�"'g�׉�p5��k|�!H{M�/l4# ��c�/`2�$^�%�i8BJY��K,.C�1��6G���5�՛A�N���Q�Ӥ��7@��2��h!�)su$�V�3���@���(��h:L���f�2��c^G���-ә�:�$��ax��Jv�!m�Qv�W0`ʄNRt_��1��	<�WZr���/�r��'hGԀ�񔘿2	��ޡF�(R��r�#��[ە�M�~�1-�8�3`������	)���O�a����{�Պ�*6�gX������~�H���#%��t�pߑ*�v��CF�s�F�x+��ES��v- j.4���M��m꾣�^vR���j�,���;�HM�yv�F���,��7�$8�H��_�F�W���)_i�]z��	}B�ͪ2K$��D�8}+��>�ѳ���ʠ&���\ �������Ig��W>�^���nX�t�u��./��.����4���W��0E� ���W�ݐ�G?��h쳻D��%h��N�),,8�8�I��9C�����-�43_�H�+Ʌ�VY��eGbTC��3��L�5o�Iŝ!��q&�( �ٚj�/�~J�	]?a����6z��.�[�(AJ�=��v'���:mN	�\ɤ��qq�
݊c9�<W�m�h	��������k�P)���>�J*r|}�3{^э2�C&��2[&i˴Pks��A)f���J4"=J�T�R���$Ktj�B�4eT�{I�i�"�R�ji�?�oˉN� �![��*�S������V"-yXW�~ϝ���=�yRyM�63N�^�Z��dn��k�]n^&;g��j���Ws���Q,[ޠ(�X�7G�~��-��<�\h���v��Gǒ`P*ݣ����۲��� ��4�hgn�`����b��1�g�wM�1|�#����V�]F�S���5[��;O��mb<|[/,�vLV��e�����/��6y�D	Z&3Tm�7��n�\{]#ꖚ��9e
�;���2�f��&I����je-��W��>�&׉^௑K$I��ߚy�SbŻ��Y�Q�d����}!�J�+����:v�fY�C���h]b��Y��sI�~��o�e�Y�t�f�+7	Yp���@%,w���鹹��v���Wc{#���,��P���D�
6����>�c!$���(��C�݋#���K����r�tg땮��رv�˘ff����%˵������s��&�R�����w>����v���}&N��Þ�*Nq�1��I��ʤ��zx������}�A�x;+�l��?��ݾ�ɍ���_�V�ɝo_�ͭOnܹq��_�du�~�q�[7���h�$�77��[��'�~'.��ME=�Z�~�V֝��G���|\7�Ak��W�Iޕ�1��\�4v'��(�C[��l�~	g� ���D^ffp5�(�+�Ji*��7�ڴu���I+�!�w�c�L펹�9X�����E�z�!64��1�z̅UlL��,�	�6R�Oq4+��-�V"ۣ�w�	j~]��m�8.͵��RI�g8[a@mjkE�؆��Z��x��fS�4��'��x'�����c3BǙ(1�?`Ys*�V"Y������u��'��.^mӏ��5�V����m��m=�cwG�zl{�T�+��i�����5�=���N[��[/9��צ+D�xL��ps�=����y/�r>G��'��'%�v��`ZU�Q����G�����-��:���x�	݊n^}a�!��z�,O$j�7�ju�F9+n�F(�7n���N��L�JW
���lZ���u�O�e
&�p2*�Sw��G�T�����u��f��4�,�l o  ��ڿ���q�ܸaů��!s���q��E�A2�փ�H=���&�)F�&eo�+��"�@+�����מ�1E(NƋr���L������3��]�Ϯ
n�Bn��|�ɉ	0��3��-�I��e*��}N���	4�-�K�@7)��L��Փ��ָio^|�JV���8V/���^��4[�}�T9@6��҅��x��.��A�@Z���,Eu������a��Lk�Z���B��{�]~��[W�������������Z�&�*η:Nm�}Uv���\Cz��Se�j�*�b��m���v�]���6_{��h����^�F��]Ol�M5O4)��5��6�G�o��l���O~���y��            x������ � �         �  x��XKk�F>K�b��`��꧎f!��!fׁ�7�d�c�ބ�B^�\�|K{\H!a����G�VK3�V���hZ������z��� &O�.ϟ�W_^�-�͋Dd'/�n�	@��$^�� 1:�<�j��H����og���^���������T2�JGS�L�dd�Q��ґF�X*Q3�&2f7cL�DE�X"SA���8aM�"�-�Zd"ݗ�2���#���W1�H�h�c%sD�4��Rٚ)���	�UF!�H�A4�T��3*�J�T�)�J��t�ty�\����$ۥ�S�!� ����Y���hc�ve,��^�$����)����8�K�<��C�{�,�c�9r!�<��o��T��!8�4	��Ɔf���/ū��������ף��Ǆa�{y�������r8yva��SF��6�o�c���X�Y�ë7�ߏG�	�e�����iw��JEڠ���;OB�BήV�-�&�,a ���(99~�DH�TׯpMg r\�Y��#!����&�� ����Vpm����q�Jd�+;�+[�)��SQ^#�5�^}�����"Q"J@	%#�� �/	*��h�GRC8�p�f�kD>���d@��=���o� O��d��O` 4��UWJ�;d�qӜ
�o7������-���r8u|⸲�{�n��W�/8�D9M����S���n�㫮R���-[r�Lt��0p�/�/�_/\���.��(f�e��֍�T#q[�I�!���̰q���柱/m?�uS�M#|�E����;І�DF��N�c� [�
5̀�����|ڽ�1�S�O����!�dh�����ߞߥ�8?�<��M����А�!�ӨԀ@����Ț"r�f"�&�5��T/T�WP��R�Ы�)�S���2y^�:�-�z-<���f}��{'�}H��7M��2����x����>0���8i}�	.�ӻ�s{@I�.{��u��J@]
N�yC�Hu�q�b�V�eC.H�l��g�1U���cb�iн%'_�����Z�[6˅�V_��g����=v~e?�m�*��Y�c9�c��z Y�$��}"*�~(dc����~4�a�!��Ke��[߹_,����.#���&��J�%��z�C/k$�ue[2����D5s�����g9q��n���o�����!�W�xW�UqȷK��ZCk��/�~r�����         �  x�͗KJA�םS����1�k/�N.݈���ŕK��!���=7���!b���!3��_�����8�3����:&kvw�MzKO��z��i�7���^ҳ~/��pg��NO/Χ����a>�?߆��>\�W}�V����������$��t[ǆ�"МI�iQ��7Y����Z"vB �5�`[ r�� �+��$#�-����-�-Kփ�~���	�8�/D8U"�$7������ ���,@�v)Nr}:4	ۨG��`k�B���a�k��:�B��GA����[�����CFqm���tZ�����]�ՙH8cY(f�E�Nz�FX�S�QrU�rGO� X�"��T���n���]�+yܤ�#N�s�a9�j�-�c�qY��_J�q�� ��$�Ō�����.�k�-Pm"p��CD\���y�%� ���F#��?�stz��>���u*��=Aw��E�����&���$'ů��$��l2�| ���     