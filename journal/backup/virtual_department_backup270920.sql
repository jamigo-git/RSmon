PGDMP     7    4                x            Virtual_department    10.13    10.13 9               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    16385    Virtual_department    DATABASE     �   CREATE DATABASE "Virtual_department" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
 $   DROP DATABASE "Virtual_department";
             postgres    false                       0    0    DATABASE "Virtual_department"    COMMENT     �   COMMENT ON DATABASE "Virtual_department" IS 'Здесь располагаются все стенды и их основные параметры';
                  postgres    false    2837                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false                       0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16485    claims    TABLE     �   CREATE TABLE public.claims (
    claims text,
    claims_id integer NOT NULL,
    sn text,
    number_in_departament integer,
    "user" text,
    date date,
    decision text
);
    DROP TABLE public.claims;
       public         postgres    false    3                       0    0    TABLE claims    ACL     =   GRANT SELECT,INSERT,UPDATE ON TABLE public.claims TO "user";
            public       postgres    false    202            �            1259    16407    comments    TABLE     �   CREATE TABLE public.comments (
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
       public         postgres    false    3                       0    0    TABLE comments    COMMENT     �   COMMENT ON TABLE public.comments IS 'В данной таблице будут записываться комментарии по работе со стендами';
            public       postgres    false    197                       0    0    COLUMN comments.author    COMMENT     Q   COMMENT ON COLUMN public.comments.author IS 'Автор комментария';
            public       postgres    false    197                       0    0    COLUMN comments.commentary    COMMENT     J   COMMENT ON COLUMN public.comments.commentary IS 'комментарии';
            public       postgres    false    197                       0    0    COLUMN comments.serial_number    COMMENT     s   COMMENT ON COLUMN public.comments.serial_number IS 'Серийный номер установки, стенда';
            public       postgres    false    197                       0    0    COLUMN comments.alarms    COMMENT     �   COMMENT ON COLUMN public.comments.alarms IS 'в данном поле устанавливается текущее состояние стенда: работает, не работает, есть недостатки в работе';
            public       postgres    false    197                       0    0    TABLE comments    ACL     ?   GRANT SELECT,INSERT,UPDATE ON TABLE public.comments TO "user";
            public       postgres    false    197            �            1259    16413    comments_comment_id_seq    SEQUENCE     �   ALTER TABLE public.comments ALTER COLUMN comment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.comments_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 123123
    CACHE 1
);
            public       postgres    false    197    3            �            1259    16463 
   complaints    TABLE     �   CREATE TABLE public.complaints (
    complaint text,
    user_name text,
    date date,
    "time" reltime,
    urgent text,
    number integer NOT NULL
);
    DROP TABLE public.complaints;
       public         postgres    false    3                        0    0    TABLE complaints    COMMENT     r   COMMENT ON TABLE public.complaints IS 'Здесь будут жалобы регулировщиков и пр.';
            public       postgres    false    200            !           0    0    TABLE complaints    ACL     A   GRANT SELECT,INSERT,UPDATE ON TABLE public.complaints TO "user";
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
       public         postgres    false    3            "           0    0    TABLE installations    COMMENT     �   COMMENT ON TABLE public.installations IS 'Здесь содержатся все установки и их основные параметры';
            public       postgres    false    196            #           0    0 "   COLUMN installations.serial_number    COMMENT     l   COMMENT ON COLUMN public.installations.serial_number IS 'Серийные номера установок';
            public       postgres    false    196            $           0    0    COLUMN installations.model    COMMENT     S   COMMENT ON COLUMN public.installations.model IS 'Модель установки';
            public       postgres    false    196            %           0    0    COLUMN installations.phases    COMMENT     c   COMMENT ON COLUMN public.installations.phases IS 'Количество фаз установки';
            public       postgres    false    196            &           0    0    COLUMN installations.to_date    COMMENT     �   COMMENT ON COLUMN public.installations.to_date IS 'Дата последнего ТО: проверка работоспособности, чистка, замена изношенных деталей';
            public       postgres    false    196            '           0    0 !   COLUMN installations.poverka_date    COMMENT     �   COMMENT ON COLUMN public.installations.poverka_date IS 'Дата последней поверки эталонного  счетчика';
            public       postgres    false    196            (           0    0    COLUMN installations.inkotex    COMMENT     u   COMMENT ON COLUMN public.installations.inkotex IS 'Установлена ли доработка инкотекс';
            public       postgres    false    196            )           0    0    COLUMN installations.alarms    COMMENT     k   COMMENT ON COLUMN public.installations.alarms IS 'Текущие неисправности стенда';
            public       postgres    false    196            *           0    0    COLUMN installations.calibrovka    COMMENT     �   COMMENT ON COLUMN public.installations.calibrovka IS 'Модели счетчиков совместимые с данным стендом';
            public       postgres    false    196            +           0    0    COLUMN installations.poverka    COMMENT     �   COMMENT ON COLUMN public.installations.poverka IS 'Модели счетчиков поверяемые на данном стенде';
            public       postgres    false    196            ,           0    0    TABLE installations    ACL     x   GRANT ALL ON TABLE public.installations TO "Admin";
GRANT SELECT,INSERT,UPDATE ON TABLE public.installations TO "user";
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
       public         postgres    false    3            -           0    0    TABLE pc    COMMENT     N   COMMENT ON TABLE public.pc IS 'Данные компьютеров цеха';
            public       postgres    false    199            .           0    0    COLUMN pc.serial_number    COMMENT     �   COMMENT ON COLUMN public.pc.serial_number IS 'серийный номер стенда на котором установлен ПК';
            public       postgres    false    199            /           0    0    COLUMN pc.radmin    COMMENT     Y   COMMENT ON COLUMN public.pc.radmin IS 'установлен радмин или нет';
            public       postgres    false    199            0           0    0    COLUMN pc.windows    COMMENT     F   COMMENT ON COLUMN public.pc.windows IS 'версия виндовс';
            public       postgres    false    199            1           0    0    COLUMN pc.net_monitor    COMMENT     S   COMMENT ON COLUMN public.pc.net_monitor IS 'Установлен ли NetMonitor';
            public       postgres    false    199            2           0    0    COLUMN pc.inkotex    COMMENT     N   COMMENT ON COLUMN public.pc.inkotex IS 'Программы инкотекс';
            public       postgres    false    199            3           0    0    COLUMN pc.other_soft    COMMENT     M   COMMENT ON COLUMN public.pc.other_soft IS 'другие программы';
            public       postgres    false    199            4           0    0    COLUMN pc.alarms    COMMENT     �   COMMENT ON COLUMN public.pc.alarms IS 'Отмечается сосояние компьютера: работает, не работает, есть проблемы';
            public       postgres    false    199            5           0    0    TABLE pc    ACL     9   GRANT SELECT,INSERT,UPDATE ON TABLE public.pc TO "user";
            public       postgres    false    199                      0    16485    claims 
   TABLE DATA               f   COPY public.claims (claims, claims_id, sn, number_in_departament, "user", date, decision) FROM stdin;
    public       postgres    false    202   �;       
          0    16407    comments 
   TABLE DATA               ~   COPY public.comments (date, author, commentary, serial_number, comment_id, "time", alarms, number_in_departament) FROM stdin;
    public       postgres    false    197   �;                 0    16463 
   complaints 
   TABLE DATA               X   COPY public.complaints (complaint, user_name, date, "time", urgent, number) FROM stdin;
    public       postgres    false    200   ��       	          0    16386    installations 
   TABLE DATA               �   COPY public.installations (serial_number, model, phases, to_date, poverka_date, number_in_departament, inkotex, alarms, calibrovka, poverka, installation_id) FROM stdin;
    public       postgres    false    196   ��                 0    16424    pc 
   TABLE DATA               s   COPY public.pc (ip, serial_number, name_pc, radmin, windows, net_monitor, inkotex, other_soft, alarms) FROM stdin;
    public       postgres    false    199   ��       6           0    0    comments_comment_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.comments_comment_id_seq', 397, true);
            public       postgres    false    198            7           0    0 !   installations_installation_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.installations_installation_id_seq', 18, true);
            public       postgres    false    201            �
           2606    16431    pc ID 
   CONSTRAINT     ]   ALTER TABLE ONLY public.pc
    ADD CONSTRAINT "ID" PRIMARY KEY (ip, serial_number, name_pc);
 1   ALTER TABLE ONLY public.pc DROP CONSTRAINT "ID";
       public         postgres    false    199    199    199            �
           2606    16492    claims claims_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.claims
    ADD CONSTRAINT claims_pkey PRIMARY KEY (claims_id);
 <   ALTER TABLE ONLY public.claims DROP CONSTRAINT claims_pkey;
       public         postgres    false    202            �
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
       public         postgres    false    196    196                  x������ � �      
      x����\�u&����u�T53Sgȱ��mv�$Pn��J��2L�
�v��A�� i�f�I����8:Q�5$^��+�I�^�^{8Y	Zݷo�5�@U�9{\㷾U�u�/'�j��������'�����h��_v������g�Q�>]_mW�a�p�>n��������������]���绅�ˑ��j������l}g}�X_[�r�����t�q�/���A�~���=pc����x�����{�5�C�Ϲ�٩����������t?p�,h����Ë��{Ή{���573x4��D���hO�Xo������(��R�o�^~�ữ�/]���;q�n(��S�a<Wx~:��q��σe�g>j�����Ÿ��v+��s{��}���k��4�C7�EQn�ڇ�������{��Э�|�[�0�������;�����݃ŭ�u��r}�����Y�o-��q���N��3��TU�S���_��_�}�Ow��ߪ�=�_���.�W]�W�aQ�w�$ݿpo�I[�O�B�)h?a����乗����f��'í�[M�6�Νxsf��h�l��NU�;��`��3�V%����N�K�"Wa�܃qb���v�o�o�ُ�Y��Uq�SH����a��)x�V��8f��{��]whh���=��ܵ3ı�'�;�/PQ��:;MY�v��N5;h`�v^e���.�����n��tk`M�8�m��Į
ܙ�����N/�98�?�3���;Bn���A3=(���~~�g��������w�a0�o���ti?���}p��Σ�����p��j���_���d�x8���@������[���7�h�{(
8_�)wE�y*�;6ÃQu0�:�2�O���n��x�m��8�����[�DL��
/H8�(�a�� <�1���W���;�rX�u���N5>���f��λ�_�C^O����"�d+
+x�c�y��+<���'N�ݢ����H��%�w��A5����hf~�-챓���Oq�TU�/�ua)��[Z�U�<�Ņ����+�����{o�%�!���)|��C]���kz��t�ܭ@I,�������]�Å'��/<:� YN���l����}�l�.:�6������;5��Դ��XW�ɶ�	��~���6]Z7ԸnDg��I���C-}��â 	�fN�a`Nf�g�TD���)Gpo܎wܛ��:_�&œ7���uE:�9o��o=�	ܴcT�wH���د�Syn�M���#�L��#�%l0+�j�+���i+'�P��q�J�zO�г���Aᴄ��.=`a���f<��S��܈�2mw��Σ�E�]4����h����g�ŉ}Y����˯���*2s[�8wX`���b�Օ�1OM����ܳ��o��h��=��櫻r����dY` j
4b��-\s��׾�g�P�޻^A��S�A��]�M;�g?��g@t��?m�s7֟��(�aG��tV�{�^l������#{��3]���)��=�V��}Vs�,��Ě�h�9��}p�`�q�@ /qD�p�d�N�O�����QvȰ<M����tݟ{l���o�]~Jwr�z��l�9	�3T:˼�W�+�+�^qq�W��"wa��.�0*������@Jƭ���Y���"{�~��8Q�y<�DgΥ��՞�s�H�>%�����Ы��ٗz �={R-�c<c���i�f�"�b�96�7�6{�IQ�;���g�$WQ��y9'���9���k�S�Ξ���m���S���a�-���2��-�[��}�J�Y^%{r�r��26����$�dN�t��c���.E@d<J��Y��u{��S� �nQ�F��%q�m��?N��ܤg��u��ω�^/�	��C6+�܋T��.��y�W0'X��ª^%r'$+��H���"3�A~�uT�9kd.�	[4pi�m?ek�l�#>g��������=�Ϟ�q��*q��x��=����4|�ʂ�ӓ}������,,ts�{�n����L��
���lAw~�W��[�[6� ��-�U�/P�{g4�)��댱���ι�~�X͘�C�]e��=��T鉇u����XH�R)�(ռ��D���+R�d����@ ٽ����b�ʻ,*?뮄7�ݠ>�u�������*����<՛�EC��sߛ�3<�hx�௑ޜꆔ�n�=�	�L�j}ؤ���O���u�S���|@CGN��^~���i�ꟿ�ޟ�������/�M�Yhx��_�O��s4:�x�Wo:��k��>I|̼74guGN����N��3<&�d ��xߚ�N]��a�,�F�抵7�f:�(5��i�@މ���]���NZ<�RO�n����_��-�� �1Z$�1�ęK��#������/X��I��>P��I{�~�7��؜��K��%s�ɿ {�P,ŧhA�ɺ ͌�Ӭn +��(y� ��_��x�)pb�	�Z{�j�3RQ��5Z�/��Q(��{I/SN��F=\�^!�<}	���Y�!�ħ��Y�����&�T�th��d�
*)T��<�nRp|i{�ü,R0���Cb��p�	�Cx�GhN܈�R�~�(�O�C������+l�%TI@R������E�BSԀE@����A]�P���x��!k���_����WT�^]�g3��-q�$|�u�s�P��2�NV��dP�a�W��#
-;er5t���i��Kì̆��/$��4�q�:2~�H��H,R�^�h���C��dB��M����PA�X{���¦'@�f9�A� ��hV��+2P�ٖT�ph�?&��8EKs0Ls$Sw^��޸_|�x�d���N���:r(��`m+J�4h�$�^xu�u��74=�����hF���絙�j�Ē=���7����;�\�0gd�,Q:�A6������{�#�
�5����z�0�ҵ�}v�x{�H(�@��1�2I�c�Zso�d��:p���t'��[�,��&~��^`N�|�o�jNI�t��}H��R*l���sz��:6�W��/]��9	Ra�{d8;��4�m����Pqz�;MY<&ϖK�U��w;�X�W�D�g�M�-;6�f|�=z��?2���n�,�s�2\�߻��w
�,��0aS������˃�6íR����kuf�\�Ґ��dH2�mj��v�"�U�8N������&�Q|ʇ��Ccâ�D�ӫ�I���-��K��։�WW9_�?�dM��s^�t��&δ���P��pՃZ|�1"J?܁�{'�ץn!4��&:Te����k-��^�R��T��sữ�
y�u��r�#��Cf�!l�,���hzP�#��*���X
</� ��q���4)Jmw��4tЂ�mZ��(�h�Wû<��#w%�����B]!����K���B��Љ��PLP�_c4�Mu�����(9�i�fq&89NWY��eX���t�O���4Hi���~Hal�za�I��<htgc����`<\G���?�K�F4�{6~���Tq��cF
�ۍg��vD�L�F<'���=^7�
Yi����e��2��Y��#��e�K��Js5E☪\�ƹ c���𪱧�ls��A���GRjqj�!̞$�I�%\�#T6�4a�08��K�i�C��i�D�p��IO�g6ٛ�W9��r�y��K�;J h$#�Hč�W8f�4C�4�ϰ4�������uvb��S�=�Ip^s�v��b7�q>��1!��u�^z3�>aN�'�����p�/\��bGB�x���D��6�w��:"�~��P.<ׅ�')�[t�{���-�'� �}I8��M�A��� Y<�!�����-(�08�^�����1�4�]lt������U&R��{�{�ܠ�	�I�m`���O$�k�)|�^dtYG�6�o�C�
�� �&�&�r��Lu����
�ٍ;����nu�T���m f�d��|��5�s���'�����	cP��1������    ���F�<�H\ঝ�����W~x���^}�������_���;������7�y���_����'c�L����H��ݥ�f2)w��}ᇗ.}������+�O~�}�'�2ˉz#�I���e&���9��ۨ�lE�9��d���1�7z�G�kYҩCQ��୺�؈�x�P{�U���5
�w�G(ѩ�eJ���0v�gt4�����]�.gtC�3��
���#&�(<x�.SE��A<e��3��l�X��L1�uB�K_��Wn�34��4���Gv��3�؍�ɺu�sK�&i�M䀇����'(,,\8��T㊁�U��K��#
y���^�c�a��i<���ù{lQ�Ļ�x1��"$��n�3[&�^sk<iv�Q�dQ{+�촨��G�duZ��Ř�n2�������)\J�l��Qil���SV"����jO��A"�da`Ǆ`NuL'�2��+�M%[�sR)N�� �����P���8��Nr�kE��<��7�BP�]5���e��W���_���Pz�ҟh�0z���}Λ=A�ɵ����f��|�Kv�u)`Tr�ꈯ�u:�8�S4<��Q>g��:�8�4�
6��x]@	��$�c�>���"�8�jP��^���~`t/�fk�p�Ȯs��C#�H�L�8a�HGG|�A��;+�aخ�F�eQ.փ�|~��q<r��ۖu8�	j{*�L�1��B8�"w�!�g�80�UP��6��D0Mt��r�[x�p�|��E������9ңg�{���E&�y��19K"l�8#��^A��,9��Z����F�R�'�"�ju*P��4���������!�\���#��t�|�����5q�Ԝ��:�l�j���VPÃac"�A�N��f�e�����Z Wf��j02�Su�f$T�Ԙ'��$�f���V�W]i?m�� ]�| �D�F�D��8�(	c��_��w�����:" W�Z��_N���>�Y��)�˙39��zX$�>&-��@��9����S�0V5)B�����3w�d$$r�,dի{�^U����cWN*�u����,�{�I�pW(����LMJx��.��Z.(�~�� ��LJ�ea|4�e���1.�o�S"
U�5��r���G������;���>�R�P֔Aӷ#����ܳ=P����"���8��[�NU[�P(:|桉W%0�S��eܞ(d��N1�P{XA�pۂRrV:����,'�K]7���OzB�S�
'{�u�Gd_7�1����tF���\��!���W%z�Mɸa]����7&�>*+��K���������5�K�`l������o�B�r�ܳA�]L���J"$�~���5a���S��8�������^�B	���Z|H����Ps��hE�839x�<�eM!ui�a�Ë�9Ƿ���:���9@�r�3/Y���t��%�����\��θ�Kw�j�*��l�C2NX�/]NG��"�f�ʹdy�.!*��F9�G�>Ι��C�)H&�!��Rq���э���0�,%w7{T)0��PU}0z����8����47���j�����[K���k.��>���j�ve��\�C	�S4pr�ם��J�>s��9U�4��4�n����8o!B���nh_�e��L>��5�9�4T���v ��Y�fC��}y�<��9�����b8�On9��d��P�
����'gȒ[���=s���S:�:,���+o�\>���~���M�#�t����M�_�a��� �4x���x�3�0�����Pmg؇ F�P�D�Vs�$��9Yr�Q�1S�	摸" <e�B�R�2���-Xb�i!����&G�$ڜ7�Z��7Qh���K|�z&��̌��)�^�!�:�Q�r�G�X�U  ����@�o�@#�y�m���"xμ��'��hə\f�u�)�÷�=P��Gd<�n<$���g����Q)A�S�|��Td2��c��Q��P<��/��Od�/�^�V+EDI�\��F�'���N)�_��R򧼅�J���p�]B�q�Q��D0;Jݝ�
��X���`���9灭~	��R5p�"<\Ƭ�_J�*�,c�ȉ9!���<bQ}��B~��q�@�C��Bz5[z��3K4հ��p���[��T�'�J�6눏"�(��I �6�;��{�Ԩ	�%VaB��S�U( ��� fZ�c�Xaq�j6b�;�a�Jx�_���G^���daA`�m!B3ľ!���
��>�G�E�좾� ��,�{�А�$G�6�d� e{�y�R���	��;2
�x�&�@w&c����ڽ9�M.C}̑.��h��)7c�le1��]�KBl�>�'�÷`,���9)�	<0�����G=)\���C�wЎ.c1���o�S*M��ec����6���[�{?6�UAyDp�T����#�b��� )�k��R�Q��P��HeE�R�N�؄�(Q�õ!=�L��g��/�NN��_g��f[isF-�����2a,P2d$dh!�<'j������f?�΄X��@Cw�H�������;/�j!q�
5�e'��p �}��Ɂ�l�rZ���t|<��S�Z$R`����(�	"�i�rJtܯ�p��v�rA�b�Ѐ8��H��e:�x+���P`jcA.Do̤کK�17�3ʑM�<q2��"ﱛE�s�����)j�㜁���?�'wnS	uN�Fմ�\uI����
��4]Xk�G����x������~�9wt�2�E�.6�-+$����w�~���(��pgRC�E:�<:�3Z�����2�P�K�;�,�+�rg2���0ݬ�84@"�a���e/�JҚʃE������O0�4=�`�����Һ��jR�-�1��M6D�S�)��-�G&|[s1TP�-���d�Mƀ
���ou���*��$x��	��֧�G�2��,��ϲ,Wɩet��*F�u��Ŝ��vĐ?�w&��׵_�N� {��Av!��pǙ���T͈��ܽ`�4H�.)�;��R��7��x(R�SŋO�,Q|�Y�x\���Gm�����P{��T�f� 5c�H�ߺ@'CP��mIG�!�u���L�5L��C�]^��pF<DO���'=�����мA������OB(H)t�h�BP��9���F�ԁ����h*�s��D�u�!�5��:6P;v�ٺ�j�8=	��Zn��ɕ�o#
�ӌ^R>����W"�V���IG8��̊���q�9��n���)��7GC��2	�܄���eimΊb���w̊1��{_����,l�CP=M��lS}A�k�!�?)�s_v�S�v�0��ݬ�|�oNO!�VX/H�W��B�.�D�����=�����m��!2|R:��di��]#�U��S@{Ze�.�>�g;�AQT:J�/a2���Jb��1������@Kj���s�Oc�*u|��H�oBYګt{U���5DNN�U8�v9 ��?bˎ��HxJf])�ͨ��r�y�k7������~Q��n��1n'�Cl��D�ΑV[3ZL���!��E ȼ%Te4h�G|K�ǁ	mV�!ǻ��{�+9�ѧ���g]�Zf��]�r�)����r�6E�-�"������a����N,�R��������E�~�$
xgW\��+q2�Y���C�wk���(���]�:0E����L���+�}��!?�R�"��B��^_U���-8����c�K�B^�2��1k�O�s6��������M�⑑�`� �V�o��S={��C����j0-^���:*�OQK�	��
�mm?��(�;$)�mT�8�T�@�����*��T:�l�c	�T�]��8�j4+��gL�q���!z�M�J�m�	�0��{�i�z�LQ�'�_� |*�S� �*��Eߠ��Am�H�B-/'�>����m���n��>�JmK�6�o    3<�T浟X��ߣ�YY��sm��L�����NS3X�Xe3�:n��ۢc�i���j
�q���г�X�����JL��>4�/f�W��e����P����`��8"������J/Б;�Y>|dk�\U��m�A�h�xW]Z;_�F���b4���10�6��\Ip&�G1?����F��Je��S��T����gu�I,v�^�L?R�x��0�5'�0!L"n�u���2V6k�o���2�M��J���4�_Wf�����w;�?%TԸ0zYz
,����8<��|����w�3�@��&���"?�9�@�t��IRG��̂���4��j�d$�B�#��O�P�����S�\jr��S�F����J��Ֆzpc금`Pᆰ0Q�r��B�N[���=�����t���Х�������Ȕ!f�s-�@h�q�.Ks��⡽����d�ݑ�S1�0nҀ�擺[�}M�@>��_�io�7E��7��j3�LA��jY�hŶ�`�c�$�$M�0m���]Rr�"��oJ�#��wZ4��$�ң��������'����r�=)�}��`������I�$����e����K��p�����(D�c��nAD�N��4۲ ���;U�ݽ���rܻ�f���x%ЬvH�-��:�(�0ro��(�$G���IH��%�P+ч��&���(��6��'�Q+l��^�^�P�6iJ�3)xx�CR���G���\/k�L�)�o�@���cЈ�X��wUk�y���l$4��Иp1F�Mc�M��m�_�� ��^�6����(�\�8��w��&��Z	[�d����i��U>(�0�"A��h�>�:R+!
�����lY��[TE�����s!+�#��nJk)�C1 �.�3U9��� �vv�Hj`�ۻ����I]��i�FÔ������ܽ���5G�����ń��Z��o�Mo�����J�`	�{5� 3�� �!Άv�c�phxS'�S��Qs�lXbl���S���2�0�ƕ�f��S��q�~�y;:����u��W��H�2���1)V[FM@�_@�WP�	�"���n�>����<uI�w�FP3D�����e�L��h}vb��Ns�o[jQ�]W۠h����dJ��Z����{2�����.y$� )��G��;b���[_8����D�zN��`B�_�P0ȅ�J}L j��i_y��N��k����҂1�qII;~�@�T*��6��q��T>�z���XzD�Æ�9��Ʉ�٬a�J�]f�#�����'C�Z%:�����*�įS�o|��ϙ�V�,�5�,����K�7�)Y�f�!�*���ه�+���������/�Ĕr�uQ���[�A;�eq��+^}y�4�;#�z��t�b�]�S��7�E�)dG�j�y!y녪���x+}�h��*�<#�?ܝ��	@��$�O�k����&�()��,�
��bg�Y�C��:�P�=r6oBͽM�o�ZY�]NJ^|7qAFKLn8�(�^�\��&*��~���LTI���p!h	�X,��I&���@�oɱ)��P�>�G�a�*�܅3荄)�È�^�1D�JwJ?Lt��޵eg8�Xκ�r#ܕ���8{�sm�)e��b���Zh�@��࿄	���(\@����
�t��o�L�e���՘�h�K�d&�H��Ppr����.�/vj��U=��W�	�l�� rY��p�C4��T3=��Ԥ	�)ߍ��J����)�H����Q��-\Rh:*j�BX�&,��08��� �	%�sC#�*��o���H�ƃ���t siґ� ԍt�j�w$,��m��ރ�$��8j�ƭ��w/Ӝ@]�ύB7��s̻�I���:/�Q/�FaP�ؔ|���c����먇0y�cL�9Y����Z��8$�ZH=����4j.�J�XH��O�����o`^�w.�E�|�cgd�VD��8�X�i�^jՑ���gi�~I�O�|c������0��f�̟OyZ&�FrL�q�R�]]]ߔ��<�g��^�E��������|q�6JsJ�'��$�xT�+�T$�ϵ^��p����K���s�1j�J,�7���d)5s$4o�6����-Ȭ�:�nU\S��yZ$����D,�MXI��/�p⠂2��P�C�BOc��rT�7��l�����:h�	�Z80L�XF*���z�� �:�VFR�m�a&a?� �loZ���8^�U �e���n�'Q{O)2�c�{y-V�+���)&�nREM�`#i�,zL��q���F��a�"@�r�D�Xp�Q
EV��[��='�����������ʗmL�²�(r�lQ�����M���/S��Ol�$�>�JwX�m8V��C��wC��D�DU���C!�DdD�R"�G��t���Q��0����JC�1\��讵��3�����;jt�!9�)���]�B(����(e;�ө`x��zP�����@!� ����2謽��-�'�	�e��.Qh l+���`YA��:*��97ve-:6kҌ֭��?�R�?P�nR�逞��$�_o��q��y��V��Y]X '���z/���/B���{�v�{8q7�t��c�b���h#{Y���t��6�:2�ԕ[�0k>f�V�눕jl���̳�ɵ��<i����y9.8��c&dlͅn�K5�\�=���rƝַy�H�R��	
-��Ѷ;�[�x�`���ą ���9�*9t+��0���С��`�
ʣ+`��������}����2�>6n=�L�:b���fkp���'�� W��b�Ͱ]'���ڹ�g�z:��!��D�J��3~�����<��RZS>aK��Ɛ��ԥ����J+����k-hw��^���v3_���ړ6`�X�P��k�i�ڒ���;>�]U�PT�(R��Ք;�`�-���0�a{"kg�ݢ��oc3�e +<���E4=� ��mK�Kx`z̈�/,k�����"�1
�Nn�)���6Ѯ������3m��n�¡����%���ׯs
�LM仿�}�.��g�BBt�55���ͤcѦPWk��q�wt-5�G��@�ԍ�	�N~@�k<iP	j��F�w�Q�'�6nb�W|M"�C�B��L��i>9�j���?= �����eC����^����3M�N��B-���z���Ϳ����mX#��&���j<p�Ǣ)��[nKɽ ϋ���~������B�~�Xw ����S��HM��CqH��l�=j!E�t��G'�Z�/0_>�Y�b�kC���rK�Zk��5������m��w��'��\�D�����|��9@
|Q�79�%h>�0�'q�>ړY��J3����<Z��b+{���b�?���|�����oo�N�􊟿��{W~����z��w���!����7&C��1sz�{�ڎVG�� >>C���֙�J�{ybk�M����)d� �ؤ>h�u�ܨ�=�ⵃ� +Ȝ�R�'�܂>ke�S��;�8!ւ��b�C��yCA{/���(��k�oX�q�<��I/�%������i�Y��	]�6�E�x'q6$q�1���ӆU�O�5�	�1ڈD�lh��U
/s/��k�����|�V>��Q.-���Tp�Oa��~�j-�ga�!?�s�}7�T6b3�813<ޓ�z�NLP��F�	۝\1�Bߤ�f��(��g�9�J��&�O4jQ��ZuDAZ����t��Y��u�w��88�mX������GϏ��j����°H�p�bUmQ�, �+KIlx́��?�/q/�'2�e�U�/��Z&SCbR����@�Q��k�}i dB�[�[��͊�l?UL�x�)�!�᳘���M�yN���"�=�R|i˸����hRv,_�O���~�iYJwo�P8ఐ@`�G������G�ʦ>\+k��u�����lɖ�mm1VJw���~Ê^���\�81�a�i��(���A}    8��qq�>��TS�@1�͆H�8��@��y e�n�d�0�y�l^Q�4��5M5f�av�㶏�ձ�4'Ɓ�����dy2[�ڂ���>B�X�4`�0�Kp��nr��C�`V�ɠ���Et/����ն�Ə���߳ �r�����*ȦY_��R?憼�.��4��6�,r�H���#M[(P)FxE�M���\����/�5!־�����+���bOql��|�1j�3v�y�7乊�f�Rev5S��{Vf�RPd���)q�zf�u@���~��w�k�$e%hi-�����HR*�c��{�>�Km��:���i��Lc�ҽ��(o{�0�+GV �~�k?�9�A=<�
�f�����y8%��Q̹oU������ߟ�e��k[��M_O�˴�j�Y����s��;�����9w��O��b�(\1��O�ร�=+aA��~6��S�"��ub<l���Q���>���_^�{�[9N��	_#*��F&�ܰ�� 
:���M��be�aaڴ_�7���-怦��[�j�SV���H>����C�f��JW_I9PB�V��ϟÏ�n���k�Uu簪Kw���|]W0��������U3�Z�z�k(�Je	0�����a"�����jҘH��c��Au��T	�!~S���f$���#��}�������Xe�tÇ��R"�R<)_X���!�ﰔ�(|�	ܢp�3����y�+^H���,|�X:��A)B�	��.��ge&�[`�D���o�&�+�X_�~0�eO�t��﷒���㔌�G�v1(Ǳ�%SňaP��^tB8@wD��V������B�!��	�Y�݄�=��w�UW�Y�;���U�A^��CB5J�0>�as䈘G~��ʪ;�pUڪ��8��,�"�Ё3T�<3��h�`.�񄴞.�~�Z���蒝w���MtR1�kC���g�����&&0W�y�k¨O�ȥ˨R9Z�EeKa�c9�P{K7�]�4���^�_���N�~�M��8��]:�09h���Cd��Zy@�� V����3�`�!|��y �O��3�j+�[��u�x���[���@G�������NM��Uz��l~
��t2����r�H�WZR����T����.�xz���u���D��Ձ�VZ9#R
����6"�=�k)�x��<0��㱥��S�����/"�z'|W�p�,)#`U9<֗�Lg����L��l9�&�'��Z6�B8o�w��=sj��V�Z8�b�l.-��8`ν�0A����%;Đ����@�1���=�dE�bi}Z5UB⸆'윒/sͭ�D2�D��i��.��(��~S ��H�%�9Əփ �;݉�0�HS��+P�c�g^yڧ�VD��kmJ_�Q#FJ�}�w��H��%[��`�t����u�Ƽ��UO�v���s�����\TfLb+0�����������ퟞ{ssr:� 0�����AL�!���T�����܆Mo�߮�C>����\��|�������W�{Ǉ��d�Xw���/#e(٢	�	g���<W璴l@����WT;�1uX������˽O����^�聧x�M�Q�z��^�#���# O�� ?����_\#�}��s�{��ר���s�P�VB���,G����r�Xf�_���i�A9���=�.H2�����Vؕ� ��mF�~f���F�4��������f�|u}>�5�����]y�0��r|�柿ML��l�#�TL�S�%6��Imָ��K�e%0[HƤ*QR*[��s3��9'��s���Z�D��BA��?�l�5�`�S$"ޘu�VŴlr�_>��q���R</6ʪQA��Q����x�Y�m4�=�@V{XC�s�r��7M2:ei������CL�O��>_��W��U�[�|��o-�N�zj�I}�k��d
F�5�I�0�3�qP~�մd�23�bs<�$�+C���׀;�(�i+6�>	����y;����q�Ұ��<76��P!*�-��JeL�x��m�Q�"�ϳ�/n�=����WQ��$8t�u���1pU�-�����elk�!�ƥm�b� �d��4n8�7�g�}Ю����r�L�M�dک��U��K�ܿ��^A,�\��T\�q�c�2ۜ��j������>hFIS�j�}�v��5�N���&� �P֯=2(mggZeg@���|J�p]���z�
�C��䠜F�)�Bw�ⱡgP}i,�b5��������m���������}|H�jga�<�l�VY�!��z�g� ݍ+,X?_C���}2�pA����9�&��00a��j"�aӤ׎Y`�X�E�pS�Y�`,<�L��C�*S�E���t6�x�I[��c�7,�XM��[+��=kJu���3(�������e2m��'ǃo+�5%Px���[3(�c��lNBwW4�%!nP,������iQ�:[,��g��rϱ1�Y�M�ސ����lkMڷ7)��m���)�����O��*���25�����F+_v�5�^}y�d��ȿ�P��~\K=��pT�"�V�=�"`j�1l־Jjg��8V��G]��QD���m�Y1B��h3gwA����v��j���W������J�itl����m[ ��m4A��x�/�v(����-���_� <�-�!6��jU9,��^�����v�><�����#y�Y��n��޸_�����B���=	M]�e�`I��@��BD���h�N� ���:�5�ѭF.��>�������mP�z���xz��=�hnP�P���81F �y���@�!���D!f��O�)]v��Z���D��̎����$%�^ƽ�t**iLP�{S����!�jU���+K6)�ڐ�,��%�=�#e�OSik�\�v�R�cYA�	gnaޘ��O��
��V{F���U�)̒s���E�y��.���Y/3�<q�m�k(��5a�/��yA�L��ȁԧx���*���| ɒ�#�����R��x)�!9==^kn�v���}��&�����q���ޝ����,�)[5�
i޷��
��+��4\y�s
j-&�z�k�^3�N�GJ���8���m@�
��9M���-���� �	�<��'@l�u�l�}?�H�0��1凂��G�����Q"�S��b��R0�옌�{�4u1�\'g�[-j�E�F����9��PPJ��k������}�����V��dI����r�&�p��~|���������5�cDu;��:w����}b"�s���nꀹ�b��uL>W�o���pR��6+M�� �q���3��|:���[���S�L2Z#����r�<>ƪ�bH/�P$+B�]y�,־�R6��g�*�������ǜ�Rw\ӱ�ށ���F�)a�*]
뀶ۍ�)|JWXb1����ޙvZ�ӹ�h��1�V��f���@��p'k�G�IXI���'8�Tk�%�٘��8`�#��D�V�+�4�~�i:U�k7Eʫ��/�kE\��`��o��|u��U��׃K�^#sj���;�5Lf��,}�Ԓڄ6�1�����KN*��|�1����
�Ά�����.( ����5���~�\@7�$���(�.�$.��=a�BfRM蜨tW�;=L�
��%�k��jvx U�p�i\��v<#��
���ӭX���[��r�a`?J~�.�x�s�$���K�ˀ�4��	���"�#��ˢ�4H�T�	�W��~tX2=y�Fm�Y��Q��@a�w�}�+�A�φ\�$�����/�o�y��S��H� ��<h��Ȧ���b�X8��y�.�����kP�us��Z&��c�8"����PJp!b�מ+�P��y1�&$�UYBpA�a��\y�v$_c�Z�,L�gf���#�^	�_�G�,!���cg�Y0�R�2�b�z�6w8%�_N����f��� tg������={:�������y��L�wIN���9���e��c���pC�1g88�!w�7�g    r[J��E�$$�ʨ���?.��#&���^gd��l6p��Q������<����c�H�N壌˦�*!yV�%�Wv�]�����drS(���X�J��ە�#�X� D̃ek�0�$U���L5z� -4d�p��qoX��AjN�%�lp%��E��B��|��%]\2	�Β�h�|6qITh��� ���I �Q7Ӎ�m R$	T�x��V������ė����.*0|7���G�3�D=�"/�EǹN��R/�L�[�5K�������j�$���T���2ŮoJz缩qq��+�"��`�2�4�h!�F}�R�eN0����5��9� �@_X"�ᩑ-�؛�rÂ�Q�ђ
�z��y ���*�Ԗ�)�D�B�O<�d�f߱�R	�%Uĝ���8���a>�d^��
�\q�/�D�ӷw9x�Xn�<=��~��㿾�G����!B�׹̌�,����Y=���A9�f�I�L��ɕ�@�B�Z�q�,�jʠ�] B�mH9�/]$��߿pq=m����\3�����(��D�*\Ǭ2E6�|�I�,c��`�d���OG�mZ���A�Z�r����u�~�Cp�'��(	�-��AS�s��p�)g[-�u���q1~x��>ж���U��@X��+������(���V�g�:K��QLc���~5����5��4��X ;��W_,�e�s�1@�{����T�8��H�A��"*u����,ȸ�W�+&����=����K>��]��Z0�]6�$O_#��X:2�T�B�_�\�$;���-��UO0�`j�(�����,�U+ı�]��Ҭ�FJ�V����L��yS��Ő?�]�3��Cb�� M5��i!��.�+�naO�r*S�b�)���K���M��7���[��ř�&�n���=I�����P�/mP�0ڧ�Z��®`�\�[� �;��=�-��K�h�����'�C�}��>�z��2��@]o���]�9V�3c�����>ר��uᜆ����~X���aۍĽQ��H���Uknqw#�8v_�{B����b�kCd���M+�L9^q�9�zRUFvP�����9��ڪ0q��Ḷ�x�i���#N��9!�MG�+�����M� !��J@�u��&#}��t>&=��}R�L����M.|�<�pVP�2?l羺��p���3mg=޼ipjE\[�����#((��~q�Fz�q~���x�N{Yn��P\�}�-|����;#eB^�
���,nI�����1dO<��d�ž�U�@����kU5�|���ǒ7܍��>:E/�������}n������D���)�� v{̱r����7�݅��L+Y���ض �I+*iM�$�dX円��KKYMQ��g����Go����Ԑ'.<\���!*��:��ɠ�$P���h��t;p�T��q0���U�|TW3��<,��+�P���Y�������$�c9�Q��x�������!�e֗�m�����I�p0ߴ)����k�¹����ۿ���Rx�{$a��.w����G� ���:!��@��T�n ���$�eKE;FC�p5l�����M�8>k*�������ۉmc���x�UO��c�L�������� I,=�o�ߢ��_����#���Õ	�f��@�<�X�Ir��X���VDU�c����vG�?�ҁ�m��?=�{Se���xM�ԛ)U'�gJ|�7/�|�I��u\|��k��*.��B���"[Ct�I^jG�E&>
���>�{�A�d�Rb�y`��m���*��	�̍��z��h ���5��N �����糽n�PA�~H<C@1{[6J�F<��HQ��}ˈv<"n����b��в3z`�_�bb�����r��p\����}z����Ӱ�cR̦�H썈�;rrz�2�?�}J��d�̻b3`�^��y�#�$U�m*��b��^P��N�FmJm������	�y��Ed,r�٨�SW�C�+w��l����Ԕ�x�\������j-RUx�H0�֋�M���Dj�]���
Aۿy7��9s�����"�_�z����;/8�0D��iޢ�v��f�m�ԙ��BG�]!A�~��ʗIhр���A����IZ<�ǖM�ƙ�}Y&������V�&C/0�M��N8vx����\拓)�2Tm��֑�wl�v���kp@�B������k�8�S�b�g���L��%	e��:b�ZoE���\�����6٤�^x�ͷ�z�M�sR"��=��K��zrE,�3�>ɿ����b=ۅ�g3�$ϱ�y}��ۑ$Y�O 2���p 0��p��:�	���U����`�.���r�-�K�Z����rOO��m��Ssp���n�wݍ�s��1���]s����tp羲�-�DS`͵L+�~�;3^Yk�9���
�*h�B�^��G+�� |;l��+�0���m,�S)gW����ģK��_���#v��n�l����(�^)���<�%nX� /�ȕJ�5x��g�4�8S��t��)��X�s7?6_1�����J^_�J��C��U����[��@�aT;@ �ܦ��͇�NL���SB	Kꆇp�`|&ǊFc�!�����k���ݪeZ�F�$S�p�p�qdIt���3����Ei�Y��ج���.Y��l1.�O��Kׅv`sb�V���$M��%N�cՂB����(��a�YK"&q
�)�m,�I�
�{n��G��㉸'~��
E�N�\��lx�MSFUL���U��� ���i���m�Dd��\c�F���o������Z�K f���4� �@�X�񫊲*� �0�1��Fch���sg�M��"�������Oj�j"���C�]�{��m�� O��75�X�������/9f����'?Q�Q�	.pbv�ǫsȸ02�`O�j�����C.�j(�o ����HB��)"G;.�l�lih�5���/ԉ��!�6��fW��`����x�i�z4uf/d?G��o�\���6p�����6$d(pb/�@m#��Q��T<�Q�`����rC�[�DaEyˡ(o��
�3�dZ��;�22h���Zf��K`�x�3�QO;b7��y*�3��j�"�,<�q��H5G��pɡ:�dصv�!bo��=�#)��[~��0О4k�3�4���"$�>���'>7�˫�C�Q2n~��*�J�Kj�Ј�໗�,�M�~���r:��<��*����
����My0;�q��&8����.Gi~'��	L��\� 8�L��V�l��C6�R :,���4�Ja�-'�L��Ko����������GX�`a��"�ȃh�.�g�x"wLT۪���=~ �5Y0=�$<}'¢CO�'%<J%�l����{/��Bea�XC2�M��M�@q���6,Ҋ�\��������͕?��O���?���Ϳx3:8\��$���탃k߲Bzi�]��e[p��]3��c�ZL:r�4j�>�ߴ�{�d;������޺�rp)��Oe����1�!A��a}:Jd�=���3K����~!����LW�>�6��>�L��,�rPơ]�Fݼ2U�Q�Z?��,<ܻ�+��쫩EN� 4 �Vu���$q��m��C/���_jB�.��D�闵�	�<8#f\�F7� �(�Tdt$��<\w^�����m��"7L�8���L�����c��bӵVP�����6
;�#�:��9�npc|I���U�XP?4AԞ˱�r�/!}S��8�>�̏�+f�MZ$�V�kce��bכ]�3�ǖ���M��{З�S($SS���ӟ���?�x��އr1��H�(�rK��#po���mW��GF�1).X�p��'�k�7��a�z�X��X��6�4��rA�m|�|at� ��=�U=z�Ll8�1�����4�������g�~G$7��aea/]~�U��Y���oK~���5�c��R�U\�Tu��N���6���:�j�Ф@�僿u�����1`ж�6    L�Q�C��w���)���X^D �V�ԥ7���E�e�߳�[�_�8ݩB��_�8�L�9���m871b�c@y;G����*x�S��Z�[g����rK��{^Z"������JCЇ>G�'�.�&)�쏃��a��,ťj�<�(�X�-�0�a�hn���(n�ɘ,A�������rLI߁��R5����~د���Ԕw~�'� c�2���q
��nehD�������Yw��9���<m��Q������1E9�ǽ����o�VQ�s�d,����y4���Z�fV5�Lt��q����m����Q��kDS��8����q{��q�
YƛI��?������K�ꃚ\���P����%��w�����8��$Pb)ܙ�:�RѨX�|-�!s�^m�����$��ësD[�F|�>��֕u��2�,��R���������}�b�m�1���b4���H:z�&)�4j;/j����{	��c(\��{����~�,*)�#����!f���7)���ł��?}(��^]���T�Y�p饶l�`�>݃��Q�K���#	��,O@	O7�1l�:��v����0�}=��@?�&�߸akA����xJQQF�QH�#˖�(_v��R9+�ʏ��ɛMye�H�(TU��<@a�!��'>���{���/_6���dV��;>^�	�_3��0�4��r[֐	X��
�����*���+\y�i�,]C��*�����x�/XJ!���/S<��4�����+G�ƽ	g��2����eS�>�i�}xOx��e<�Q��t�[�	[<9���r{<�����K�Ew�_�xl�*�xm!k3~�����
�*���;`�(���d�v���D��{�)�#~��R0(ݣ+���ߵ�����c	�LJ\i�φO�W�#^A_��Y�4�FP�37s�:��Dq4�&�a3�6SO�;,v0�v�_��J0>J8�����?�ݦ����p@(9����k��N>�ԎB<&l��w�
�u��j�ҭm��Xʇ��dһL}�����jJ�H��o�~��4%���|���V��M� �]��ϣ�PP�9��q��)��N9��H��t�80�J2�����6��ȸv^IY@xu�Zp6M������o�
ϘE��k[J�a��Z�S�X���y~�����o۳�A���L���,����D�-�cn�.��-u"��k�d��T�<&\�W�{a֯�?8^�u����@�yY�H�ݠ��aa��o7cjV��t����ETP�Ǥ��w��R��̔�1�0�\z ��9��\2WkI�@,�����0��1�d!�qԘ���U���cZ/�`�rJ s�k5B����Bx�V���ٹ�0�����Ɓ�ּ5g�>3��@<wv���4M�u-JU�UǢ���Y�h�-����fĿ���릂ʯ|Z�ӝ���_u}�Kdݑ����l�X���V�D�.�'��Ԧ��̫V:�[a+��e,#��,�"n���I�Cj�Α��%"D�«&A|�[�pz�5aWJ�	��D�z*��b�%�e44�Ǽx�u�zd�h����s{��6ڌĬ�tp��L��bV���Q�zޠ����n�g����j�ֳ��rOj*��Y�Z[~J�G%��E�S�_>��j&��(���U��d��2�^aY�ۃ�C�# 3kiZ�!6*�D	�!�?�<�tt�c��Z)�"����8^�{W��
��%��X�R��`�s�bN/F�	i�BC,���;��j�3%�k��TSdoJk��UD�iJT�6n�i��Z�U���d2[�n�V�0
���$�gڎ.T<"�<�\%�1{��z�jg��_��(�)"�cF���F1�0z��\��.���X:�`��w8vu��t�OQ���59������Ľص�.e�C�q!�)���>E�wͭdJ��t�~�S�����e���;e�%%��ڌ�H�2i�iu�i��+�/aG'&��#����J^A���_n���b>i@��u���쯨��Z�#� ��Y�	f�g����F���P���:SN����~U��	E�ԘJ���1%�jv���fל��G�ٳ(RDG~��7O T�.������?�� �01gI��iԟ�8��MnxIl�emEEO�����X'��֨��L�wa�q=�����#1]��i%�Ȥ2bw)�3�D��_%,~+���c�N.�Ш*���
���s�@��8�C�����kZ�d8x� �!T���U��YJJ�8�L�w�k)����:ł0�B�oSDh�������A̫+cS<�3mCc�B�� %e�v�+QѸ��ě(^ŋ�����&a[RXµ��~�.����4�R?�T�ݩ ��35�]�._h�ه�-4�l�-"Ǧ>Ӥd7����}���5R:�|�J	�P�r7D{B�������%(��_Fl�`�|�|��w�;�W���mrJe48E��J���y�i�M��]��T5QԺ].�Y��K�@�ڸHP����c��ǸD`�M�~a˓�[	x#�^bcP��;�\�=��_����p��e�)�xW-���RK�{�h�����<F�j~f��7��^n��N��"*�1��Xd"3d�5��4+�^B�9 SW���o-l�����"�U^����!�Jٴ(Ph���1�Zg�6P8 mPXL��b֟�}��zc����L��d[jJ'C�q,�*�D�48jgB�yY�_�g��Z��g3S��C`%ǌn$P>N�eR>i���LA�C��l�����0��{�r�$�j����6�$u ������ )x�w���V]i����3-1�ΈZmn��;�<�
]P�lo;�n­��2��+����w�FN��~D-���]�s��D6�F�lg�A�\Y�.�~�zn̔�jù�I��2���k�bx~��$��)���ibʐ��Յ�8�D`Q7�(�9�vk�I7Mħ[{@�}މd����~����ډ��,��*(h�^����k��f� �cZ3����`X��ƿ�kk,Y#O�>�t��>	�Ŏ�RB��$wY�3�4��Y��l�����i��ԝ �����X�|�%on�bO��Ӝ3��UbS�ˀ-���k��v�Ô��枰� �n�
oE�Ma�e�̙�|泵��=�@�ڳ-��;�W��g����]I}0D:��H�]M�^���[rNm��2��!���ۜ�*1K�teH+�݋{�.��W���ӗu����W�/�so=�%-��2�z7NJ��� ���s��j�����`�]���%�n:P����]�<��hbj��!��+��^�>L�NB��Na[��vV6��V��İ�jlɡ܅2��IkrR��[�f��� ��ξG�5�Pj�3xE�WGz����#*9�.T{?xU���]z���k���렧�QN�g�=�c��R��N�j\��hv����sЕX>92��`�	~����I���E�}[����Eҁ�:s�Eڜ��n�4 m`��{;�G���rηR�)��*���
\����NL��c�
J��u9
!��[����<3~�s/<ߣҢg�t����yed�9$l��'Jƥ�0tn"d�s\����ܴ��)�+)���Mi�+����\�))���,Z�jp0ڥw��^rx%L��j["�T��=q@�J[<��l�w㋤A�)��x=���lO��� ,�VzG���|w�>PF&�Ж��܅렴|�ڬ������F�J�f@�t
)�Q�YT������M}5��.=�1�UYI�*�b6��xRn�B��ڿ����]m��m��p���������3� � ��2���K��@]�o�~�ާ�I(Οn�ҹ��F���ߤH=�5N��d\Q��P���<a�F]�6���$aOI0Z�Y����uSw��\��Z���Bb�9��R�#3	�>�yͥ�,��I�lY��NG�z��Լq����]�]�qd�xh�i#4�0�r1��� �
  T���ډ�ՙ�D8�ma�
0$�ҍ��c��J3���u��z,�s�Z�$�h�F;�q�H�\X�3,���q?�C��/�
�����
��EJ�Geg�a/b�v�{�0�𫽆��o��0�Ɨ�F�"�g���!������h�^�ݐ)֚��?�`(��� �Gm� �j��6�	�n���Ck&��3N�Uw���,w����7)}��zC�'q��+8Ix��OM��;X�칯>&��kT_O��\Pʊח�!�����W�����S�R2'��n��ɜ������(��^I��\�%~i�����+[� ;p��c;gd����\$x��ѣ�1��jw�Ɛے�gc=��w�FٞM�h�3{������S�_�_�����K���:TF����
����C���fj�-)�IrF�e�!mv·�y�R�n�������\� |+P��Ըx�/^�( fリ�m,G~�Ɲ�M�9���U��RAB본b�ƞ��-h���U�p?���L���RF��'�o�i�ɅC4Jq/
��;i`�3��s)��Wr����,2��Rw��"Y[����0A�*�s��� +;�~+͸�&	C�jȤ�&��z/s���PP$����0��5�"��@�^V�2�C��.�!:ё���6;)�(.WG�,?��Z��%Bч�~�*%:�#�S}0*���Xp4�d�B#*�^~��7�ꙅ��6���K�}�z�0l4l*�����
WVh���Jg-����@�#��:�D�@W�C���dp�x齟��Gx�y���᏷X�|]�(:��8n��L��{�{�c��|�4��F�D�ޒ�RW܌'Оl4Vl�o�*ósm��!�؈{�'3]%r*v7�.4)8k�GS$�A������Us@���p�id�5q�5$E\�}�Ȭ.�S��ɼ;��GD!0(6�Zc�#40Z줔�q$��4_�[G�:uZv&ƨ-���}�lY��3�4�༾k�Nkh���`9�#�\��[�m�A�+��)�4?ȉկ����×�=Y(]�x��D:=4G-1j86�Z��
Z���7Ͽj�7�\{���ב�8��z`³��"a�w�(W�'� Gюě��9��i��V{�טT�&Xg}��r4�
�Ża��fp���eǱ��3r�iP���(!�ٝ�$���Rpf��채=��!H�"���l�U�+H��ZA����Ĳ�Q�d��"����Y�j!��C��=̛a�$�W��].�s�rR�,�bͶ8�\�$�ti���!�D�`�<`6].^Px?�+(�r�B��Ҫ��[���V5q��B�G�3����"O]o�ں;G&Z�"��Z��!���J�Y8.U�-1l.�S?���Y��uү�(�߬x�#�Ij�fD�(�����D��a�4%��/�l!�I��yq*kg�W�S���f!��J���p{�Zu�\����������F��8��3V7�)��V�}��E8�}A0�"�mO,#�xLļ]�d(�����:3��m�]e^�Np���T� �E,t�dΟ�ƣ���_5P�=��І~bFgh�d�������pF G��S�n<���y&��Mݮ�۶�\۶[���8��\�[e{2�{��U�
=���Q��%�+ H�sq8}5-a��ls�Q�g�dB��ܽ�S�IkX0�? ;���,	4=&��B��������,�,�js�	���r��������ܿ��Β���r����?��?�W����� ���a��cW����P���Z���D�uD�L�=�� kw�	F�̵����w���^�CA�,�^=��r>������5��pt��B0��� A��.ۙ��h�f�jm%�����O��7�N��1�.�仞�'�O�gC{��h��:���
�[ XR�XZ��h3��^�d}�#�[pv��$�f��77��榷�V�,��9�.D��LÙ�IԘ�w/�a�Nb�Lk<c�t��J�-�S�٨��&�~]�d��66��z�i�-G��n
E��E^|y"V��!�+7�`;�د3���9�nR�\��):�1�
Lܛ֜I� $vU�E��X�SB/O���k�O�/�*�&�Ÿ��|��E�6�+�������T+/�����~6Jԛ<G��_a�%U��8�pਞ�Q�Y���v�s����;Iˢ&4,i���ƪ���.k&����V�b3t�~b:��y�`o��*ceB � �:�m�鄩Ǖ-��Tg��W���(�����^�'%�N�ĵ��,�^0��A�i�Q����M�<�hP��RyDԓ����p�wߛ#�H}��{&�K����6�Kt-����z�o��D��������R�_ڼm°&bUY�i
��`��
�u��V�"��䠚fw�{�l}���3b�6�#Yh�Շ�;�D~��5��J��T7�09�L<c��[(m�%?f�F(s��A�,�h�\��>��{L��Z^�۳L[Yo)��y��`����;P9�v#f��!��v��e��s�Qt/��c�}��ٺpf����[ڙ9c������^�u~���h`}$}���I��aؘ����MG�s_�K�UJ��>p�tU�T��E�=Ɛlb�@��0�.��V��!�G/B��0�0���S3���접�B����~��_�H�            x������ � �      	   �  x��XKkG>���=ڠU��0�$"l9��B�+9!���%�� ���GCl	N���?J�����jݑ@������-/o ON�O�/�_��˫B�/N�g� � �?^/uA �_�o�3Q�/�-���o�7�|��e�S�wh&e�RyT&��a�L&��7�*��)�K%&�fBf��j��r��f�L"�Kd"�c���'l�tf��%�(�lf�|.�����d�_ͤ2�g�U���1sS.��5L>�%�
�B2��l*h�2�gu6�n�r)�JO���������n��Rm��(���b���g�Ȉ#X�wcI_a����xЭ���E���I�;j.�7�0J^���MJ|i�//?�9�_��W��[o-X����B\H�t��2�p��ޒT��?.�`��������Woʿ>�z��,�}�ŞP �$�DV��/!(N����������i��c|&/>���Q�5�F��!���Zr���������;�@R�ߖ��Q]{$�������"����\[T �<>��~9�	i M��SI#��g�Q)ʋg�:��7��7�������7�\�[�
NC��qU]U�F��)P="�Q$Zf@�(�T��R�g@�t3i ����ĂD�A[ȥ��v}!�L��b�㮫*��YP��)���&=�-�^.�=&��@`�?j�BD��I���5�S�`����.�G �c�]�uC8��"�1��jyl!�t��^_-���gו�c�R/��Y6t�	��`x�z]�{�3�ףՂ����S��i!�>lc����?%���@m�k΁C3�Ӆ䪶�W0����{.˥�ƅ�2�F��Hl��i��`����'N�XO@l�j:}T����G�?�X��K#�+-���^��P����!�X/��aEW^�Ҫ ��h#��'Q�J��a-����n���L��Է.�F�Hj�I� yf}R�=�f\.�ړ~;j���ԭ6�ل�C�ڦ�:@�ؚRR�N��[�z2iz
�s/��Plj\�QxF���P�2�t<&a`�/�v|W���t����*����=l�L폔菰%���O����]����\�-��e,6r	��q���9��Pm� xF5PŰ�v~�ډ:�*6in�QI�l';m��.�9�����n�c�3�A1l��А!s��"G���}K*�Í����KB��t�X{4�N��.�>p��q��8e�}�[�L��[���[��C��q�L>۝L&��R�         R  x��XK��0]�O�'��c;�/лa��Bb$X�Ċ%��-$��`8�s#��3�����)��Ī�g׫W�(=����:i`�n�a��m���>L�]���>}K?ҍ]��n��]�|�������6:����v��~M��O��=����7�V| '$^�c�n e����Ck�Z�B�C�SRdԥ/i�?T	���"�ė����7 L���8��� ׄ���ADAh��⹨��J4��
��d-� �Z�����A���n �� �5�I� !,��j0P e<T\�쿩�7��l=�,\��
�2ƶ��B���B�I١�A�[���3�S1���f�u�Ƈ�1��<�X��:
�u�n���n9���H�\l��@v>���{�6��޵'�l����J&:$bf�<V���ap]�f���z�:  ���?��.C#ke]�<J����RH���Eu*g�|��v�qRgg0VE`)�~����Y�������:�9��
��ܡ�-O\!�Ut�d򦈍@HQ�,�'�d*�>�dl�[@�-e}�4i�b�qX�
ġ���9�[���j��)S/n     