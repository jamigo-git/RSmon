PGDMP     .                    x            Virtual_department    10.13    10.13 /               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    16385    Virtual_department    DATABASE     �   CREATE DATABASE "Virtual_department" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
 $   DROP DATABASE "Virtual_department";
             postgres    false                       0    0    DATABASE "Virtual_department"    COMMENT     �   COMMENT ON DATABASE "Virtual_department" IS 'Здесь располагаются все стенды и их основные параметры';
                  postgres    false    2821                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false                       0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16386    installations    TABLE     9  CREATE TABLE public.installations (
    installation_id integer NOT NULL,
    serial_number text NOT NULL,
    model text NOT NULL,
    phases text NOT NULL,
    to_date date,
    poverka_date date,
    number_in_departament integer,
    inkotex boolean,
    alarms text,
    calibrovka text,
    poverka text
);
 !   DROP TABLE public.installations;
       public         postgres    false    3            	           0    0    TABLE installations    COMMENT     �   COMMENT ON TABLE public.installations IS 'Здесь содержатся все установки и их основные параметры';
            public       postgres    false    196            
           0    0 $   COLUMN installations.installation_id    COMMENT     m   COMMENT ON COLUMN public.installations.installation_id IS 'Уникальный идентификатор';
            public       postgres    false    196                       0    0 "   COLUMN installations.serial_number    COMMENT     l   COMMENT ON COLUMN public.installations.serial_number IS 'Серийные номера установок';
            public       postgres    false    196                       0    0    COLUMN installations.model    COMMENT     S   COMMENT ON COLUMN public.installations.model IS 'Модель установки';
            public       postgres    false    196                       0    0    COLUMN installations.phases    COMMENT     c   COMMENT ON COLUMN public.installations.phases IS 'Количество фаз установки';
            public       postgres    false    196                       0    0    COLUMN installations.to_date    COMMENT     �   COMMENT ON COLUMN public.installations.to_date IS 'Дата последнего ТО: проверка работоспособности, чистка, замена изношенных деталей';
            public       postgres    false    196                       0    0 !   COLUMN installations.poverka_date    COMMENT     �   COMMENT ON COLUMN public.installations.poverka_date IS 'Дата последней поверки эталонного  счетчика';
            public       postgres    false    196                       0    0    COLUMN installations.inkotex    COMMENT     u   COMMENT ON COLUMN public.installations.inkotex IS 'Установлена ли доработка инкотекс';
            public       postgres    false    196                       0    0    COLUMN installations.alarms    COMMENT     k   COMMENT ON COLUMN public.installations.alarms IS 'Текущие неисправности стенда';
            public       postgres    false    196                       0    0    COLUMN installations.calibrovka    COMMENT     �   COMMENT ON COLUMN public.installations.calibrovka IS 'Модели счетчиков совместимые с данным стендом';
            public       postgres    false    196                       0    0    COLUMN installations.poverka    COMMENT     �   COMMENT ON COLUMN public.installations.poverka IS 'Модели счетчиков поверяемые на данном стенде';
            public       postgres    false    196                       0    0    TABLE installations    ACL     4   GRANT ALL ON TABLE public.installations TO "Admin";
            public       postgres    false    196            �            1259    16401 !   Installations_installation_id_seq    SEQUENCE     �   ALTER TABLE public.installations ALTER COLUMN installation_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Installations_installation_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 123123
    CACHE 1
);
            public       postgres    false    196    3            �            1259    16407    comments    TABLE     �   CREATE TABLE public.comments (
    date date NOT NULL,
    author text NOT NULL,
    commentary text NOT NULL,
    serial_number text NOT NULL,
    comment_id integer NOT NULL,
    "time" reltime,
    alarms text
);
    DROP TABLE public.comments;
       public         postgres    false    3                       0    0    TABLE comments    COMMENT     �   COMMENT ON TABLE public.comments IS 'В данной таблице будут записываться комментарии по работе со стендами';
            public       postgres    false    198                       0    0    COLUMN comments.author    COMMENT     Q   COMMENT ON COLUMN public.comments.author IS 'Автор комментария';
            public       postgres    false    198                       0    0    COLUMN comments.commentary    COMMENT     J   COMMENT ON COLUMN public.comments.commentary IS 'комментарии';
            public       postgres    false    198                       0    0    COLUMN comments.serial_number    COMMENT     s   COMMENT ON COLUMN public.comments.serial_number IS 'Серийный номер установки, стенда';
            public       postgres    false    198                       0    0    COLUMN comments.alarms    COMMENT     �   COMMENT ON COLUMN public.comments.alarms IS 'в данном поле устанавливается текущее состояние стенда: работает, не работает, есть недостатки в работе';
            public       postgres    false    198            �            1259    16413    comments_comment_id_seq    SEQUENCE     �   ALTER TABLE public.comments ALTER COLUMN comment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.comments_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 123123
    CACHE 1
);
            public       postgres    false    3    198            �            1259    16424    pc    TABLE     �   CREATE TABLE public.pc (
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
       public         postgres    false    3                       0    0    TABLE pc    COMMENT     N   COMMENT ON TABLE public.pc IS 'Данные компьютеров цеха';
            public       postgres    false    200                       0    0    COLUMN pc.serial_number    COMMENT     �   COMMENT ON COLUMN public.pc.serial_number IS 'серийный номер стенда на котором установлен ПК';
            public       postgres    false    200                       0    0    COLUMN pc.radmin    COMMENT     Y   COMMENT ON COLUMN public.pc.radmin IS 'установлен радмин или нет';
            public       postgres    false    200                       0    0    COLUMN pc.windows    COMMENT     F   COMMENT ON COLUMN public.pc.windows IS 'версия виндовс';
            public       postgres    false    200                       0    0    COLUMN pc.net_monitor    COMMENT     S   COMMENT ON COLUMN public.pc.net_monitor IS 'Установлен ли NetMonitor';
            public       postgres    false    200                       0    0    COLUMN pc.inkotex    COMMENT     N   COMMENT ON COLUMN public.pc.inkotex IS 'Программы инкотекс';
            public       postgres    false    200                        0    0    COLUMN pc.other_soft    COMMENT     M   COMMENT ON COLUMN public.pc.other_soft IS 'другие программы';
            public       postgres    false    200            !           0    0    COLUMN pc.alarms    COMMENT     �   COMMENT ON COLUMN public.pc.alarms IS 'Отмечается сосояние компьютера: работает, не работает, есть проблемы';
            public       postgres    false    200            �
          0    16407    comments 
   TABLE DATA               g   COPY public.comments (date, author, commentary, serial_number, comment_id, "time", alarms) FROM stdin;
    public       postgres    false    198   Y1       �
          0    16386    installations 
   TABLE DATA               �   COPY public.installations (installation_id, serial_number, model, phases, to_date, poverka_date, number_in_departament, inkotex, alarms, calibrovka, poverka) FROM stdin;
    public       postgres    false    196   ,C       �
          0    16424    pc 
   TABLE DATA               s   COPY public.pc (ip, serial_number, name_pc, radmin, windows, net_monitor, inkotex, other_soft, alarms) FROM stdin;
    public       postgres    false    200   F       "           0    0 !   Installations_installation_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public."Installations_installation_id_seq"', 41, true);
            public       postgres    false    197            #           0    0    comments_comment_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.comments_comment_id_seq', 106, true);
            public       postgres    false    199            �
           2606    16431    pc ID 
   CONSTRAINT     ]   ALTER TABLE ONLY public.pc
    ADD CONSTRAINT "ID" PRIMARY KEY (ip, serial_number, name_pc);
 1   ALTER TABLE ONLY public.pc DROP CONSTRAINT "ID";
       public         postgres    false    200    200    200            
           2606    16422    comments comment_id 
   CONSTRAINT     v   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comment_id PRIMARY KEY (date, author, commentary, serial_number);
 =   ALTER TABLE ONLY public.comments DROP CONSTRAINT comment_id;
       public         postgres    false    198    198    198    198            }
           2606    16400    installations installation_id 
   CONSTRAINT     m   ALTER TABLE ONLY public.installations
    ADD CONSTRAINT installation_id PRIMARY KEY (serial_number, model);
 G   ALTER TABLE ONLY public.installations DROP CONSTRAINT installation_id;
       public         postgres    false    196    196            �
      x��[[���~f~�O��$�&Q�[�� iS�Ї A�@���h^�Z;v���v/1�r�X�V���P���%��9<�<��E�x����9sf���fQ��n{ſ�u1-V����œ^��ߗw�E9��Y�,2�x������n�|�|�o��?~yRÕ)�2-f�Z?aU.���/�E�?�-� /.��6|��X�Z/��~����oYL}Z�^��[�-���v�~�ņ޻���Sp�D�/��9�}9�MÂk����_Q��<�µ�e礙uyr�]��/f�������}�Ƈ�Y4���}��-�jꇑ�����i��䊥@��p�$=���W�CINaK���
%��Y�������hK����}\O ��6���|xM^l� �D���0���Hu �Y�s�9�ՠ�PG��E������=�B�wU��҆>��Z]l+�ER-
^�:��ds2Z�؇�)�e� ��M��hL�4��]��^�0@P�)����wq�~�Iz!�������ʉc�����ID^�����R��7>}#"w�w��W|���a_��{�W�$md`YYy��у.�AT}�+�5|����B痓Ll���|�ʷ��]�	ǉϴ~��^��� y��G�8��ޯ��ڠ�[rW�����Uv��1`�aӖ��VP�-}�<E���f��W�]|SF+�vpi��MA�����N#N�0�������b�fBrl`���5�?Ȗf�"��m8���k,��c���9z�z`a����BԘ��I�YG�1���G|u��k�7> \��P���/i+����m�H�`�l"`a�j�0�i:l����G8��+����َ�W�td�Fq�q���؎�9+�[	�� X��_�'*���Д����pp;�G_т�����>=�P��3q����ӯwQ�hpR��v���ϻ���{m���U���ʑ�V������= @M����nH[�*ՀC���	��(Ҭ�K<�7;Z��H&�&hG�sO�|�a}$ E^0q�zG�SxzK��B[�9��B�A��n�3�S���2��!����0� ��9�]��U0ldU
#�k���Ʊa�n,��!"�!
���A!�#(t̓E��(���b��h��оUa��f�h&k����n��1eg�b�$Wy�-��ޜ�aT"�\�X�b/H���'�����~�x��a���^�<�hض܏�SJb���k#��S��]�y� �
G�LE�-8��M�U��Sg�ae���9L}q��[F�^Ha(3��yA�~�$y?6M�:62cTn��;�^p)� H%��` �WN�� �H8B� �������U34h�Qeڄ�s
"�VEA@��O��V)��k��<��Q�'AA?�ݡ���6������2���C�D%1T��|2�!���>�pVxe��Q��V2�s�Z���)ǊV�����x}��ɖTu��X�t֨��x��P�r ����Џ��3r�����0�<��-�n}4IG�8�0��YU�]��B�R�^1��t�+��Wh���2)�8oc�Տ��������EǮs�>�H'ҙ�~3+?3�BG�3:[��`U�5�ׂ�-�A�B���24SȪ2zA��%��1��Q��gO�#��wҁh;o¤�7-�]��aS�b��\���:\�rT���Nl0	� g�$%s
#�"~�m�t�����9O,�Z4z��L�?C�/��Ӎ�~���_��J��� �L�E&,I=�)��=���a_�=�&H?Wy�s��u��V���j���C'�g,�1���ZJ������V��͌^� �i�3��ꍢ�C���([�F!�CV�	�ʎř%?��}"0�T��$�}:���\���%i���a��,�"�f��R=�:We��l��v7��h����"[v;R�ׁo��yIp)��c�T�9�U��Xw �]D������&�&ᆶ\')�ƾ}R*���:}�$k���UL�y"�;gS�k�P�mmM��H3_<���r fR8I���(�3�� !��@QOY^�wX�`G�M�J�U�F�S�f���0#N�b-4�G(��/��ڧ�fM~����������O�!ި�{No�҆.�}/��蜗r.0�Y~��CZ��_e~�C� .��8�:�G���o�E��E_���5�J���oи+�<u�s�
���d64�ce_(�9�&�.:�.^���j��g`09F�2؁e��`��+A�o���]���hw׃��*�X��4G=����+7�Gf���0
Ro�T�s�^������A�5*F�]Z;�Q��`'K����d��T}�Lu�w�ە[��4q�&�0�o���;f%!w��Dez��f
�^(Js�X��m��E��� ,rT�0�M�a"��g��%%�*�h?IC/
����=l;w*��"I�C���9#��.r����ȹ���9
w5!����l��;j�8�q��J3
��I#�P����:�S�~��/%�r��R^r��@�0��V]S T͌��m��n��	"�pjU͂W���ko޼��c�xi�}�[��i/)���J�s5`lC,2	�5����K�1B��$�V��_uE�T���/�m�	�8�Ҥ��<�	h3����>x��X�[� l�-X�Eǌ�܃�Xx�R��߿��5�vCǻTN9�R�ѷ��,#ǀ�}�՗N�L����邠�.�8�)WҨ�9f	"�:��^��e
�e�<��h�LW���Rđ1t�G��ajXo��s�3
��1�ҫ����n9N�H���o2cUn�#�yi�f׭��Ӯkn�ج���aq/�<t0zQ���t{juP���+[�$���" sF^�6���� ]|���D� �Ӥ��9�1�E�a�V��6>�1�ɣ�I��݀Pl=Uyƽ����p�n����=4YZdL�Cl�35d+v�'6Y E��L,<SU�\wi6�Iy�$�Ġ��\u��)��,:����*B̬>�5[N,����.q�� $�T���	���%�Ba�7�e��eai?�~���7���c@"j����n䰄{�::����ܨI��[�����S�����A�b�Dv
��ɍ 	�DhԬ�����H:��W��J�T�tu��%&�p�F��q8�n��P�u�;�ym�Kn³6A��ܗ��dՄ��S���:����ޚ&<����U��F l�71�������|lF=�F�aBQy���{��&.ď�'�e��N�U8� ZLg�@�/����[4��m��4�p_iZ�(F˫AO�]�o�y��9}��n0L��S*������q�z���;v�FZ��X��J�TD�a5	���HE�>F� �#����o�kfʿh����J�%�XE6#VY���� R���x�cJAk'=z�n��Ycv����Xo���f"�TR����}�����G���������W���U�cýF�C�jI��	�I{���pݥ8� x���v�+�a���:,8	��LBQT��[�#Lr�f���DΓ!2������18�,W��c�3�g��-�C���_��P�ȋ�}����v��"���w���6p7�1�X��^;��� NŶt/%�P��V2*S��Ѓr(
���^�g� ��ӠH��Uh�V��WQ�b�cKA�����������U�|�Y\�8ht��1oU�
%�20$��Bѵ��'{ٱ:5>�Fz�ɶI����wW��q��4�.H>��nE���*��蟱�p+4�/7Ш(F�5�ՠ���T��%gXp�г�t�5��k�E�ܷ�Ӭ%�Qɛ|��]o�/���x*�fƵ$	 ��?P�B������n{���>���C/: 1��{�����(����K�̜��͋�7��vL���ߋ��̬j��P���J�b�<��~���xJO�6e4�ϑyG�}�#�j*�V�Ӭ"��T���W,�Z:��&Z&����Z���B�ך��T;n����\�T���Cc8e��ש��9�J��ю/ �  �1<�Q��ym"H}�����u�3�Ȁ�q2��?Ɯ�(_��c�v
�P/:Ld�`f��z䄨0����s���4�������\Nd��9۟�Go(��ѐ�\w��}W&��I��׿���������Qě�i��*$��_�-b�۠�[�ѹ/�� `޴�6�03�x+o����]O��q��u$X��g�)���m�����h�w�[.p;�_�5X� 3�l��hA�x�E�h��B9Zϲ[��Y�+�SP�,�1�[��X�c�ر�Й	�e5sup�����4�\0$(Ή���}�C��R�5��� 4��R�[5u�jCę�����]� U�Ԋ��L�㾻.�)�3eb+�8sEc�����4k�ԀG˜���3�k��y%4�
 �Ny��N�!�̸M���"�M�����s]�6�爫S�,�1���o��_�      �
   �  x��VMkA>���[h��1�;{�x�j�
�J���	I�x����S��QԿ��G����f'$!����3��<�QP�{Ҡ����d�W ]@��]4�J������ˋ����np��t:�;u��w��ޓ�w�^�ɣ!4�5��R�
�5Z��KL�J췃���Y*C`����)��/K�P�g@l�X��4
������WWg�˓�c���f;zk�q��]��|�~T������lN�y�ԣ�NHk㬁+	x�S�l�5Ye�ղ9��p��X�� �Ng��;y/����^�R)�c�1�P��Hl�SS�H�"^�������T�~-!8����w��΃\@=��t�l��F4b�p�h9~���Y�����	��(��((�	��p��)[(䔦�)��S�R�BaN���k�\����@��6ڀ�WtddQ���Y���C�1+���B�M�!C���T��/���6�_=��n��i���t)�t��T��gC��i� '�0zQɜ���Ǒ*�z#���C��h�1�i��m֞E���L�7yӡ�c�h�������u~V=B]^Pb�Lk��4l���Rr@�����z��h0E�#Dw��@�bfӋ�Ɋ�!�Pq�d4\�Y�U�v�0��D��U�x~m"6�D\�հ� ���e�B��o�f훨_.�1�m��a�1�ذp�/�&���u�Ѯ������      �
   �  x�͗�jA���S�	����:/��.R�	��B���T)���� H�g�{�̷{�X�8L�+�I�c~|�3�'YqV�"CE&k��M>���c�>��^o��1���ޏ������f{��^�G��R�<�w��x���C?�������o_�'$/��886L���L���� 콉d�; ��jk�+� "v�`[!�):AXW!�ˉ���\X�h�X�d�Z��&=�;�"�G��t9
��E�C ��Ч]j�H���ڥ8)M¡S�N�*$�Tg_kL
}k���?����U+e��Y\�XKD:��\������A'�6#	,��L�9^��
6K�F\N��)K�5�u��.���ia)�&͞q�x�C+�T��`q�1�"͉�OR���E �)��1�j�pW鵌�^hk�N�ܡ�P�N!�8g�w	>@� m�#��¶��99��Gc!���D�69�ʀ���W��k��pU������b��=��     