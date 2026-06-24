import re
import os
import random

js_path = 'sains-darjah2/script.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

images_map = {
    'unit2Data': ['fox_peraturan.png'],
    'unit3Data': ['fox_tumbesaran.png', 'fox_membesar.png', 'fox_pewarisan.png', 'fox_tumbesaranku.png'],
    'unit4Data': ['fox_beranak.png', 'fox_bertelur.png', 'fox_kitar.png', 'fox_haiwan_membiak.png', 'fox_membiak.png', 'fox_serupa.png'],
    'unit5Data': ['fox_biji_benih.png', 'fox_kepentingan.png', 'fox_keperluan.png', 'fox_urutan.png'],
    'unit6Data': ['fox_terang_gelap.png', 'fox_sumber_cahaya.png', 'fox_kejelasan.png', 'fox_bayang.png', 'fox_permainan_bayang.png', 'fox_wayang_kertas.png'],
    'unit7Data': ['fox_bina_litar.png', 'fox_kenali_komponen.png', 'fox_fungsi_komponen.png', 'fox_konduktor.png', 'fox_mentol_tak_nyala.png'],
    'unit8Data': ['fox_asing.png', 'fox_boleh_larut.png', 'fox_larut_cepat.png'],
    'unit9Data': ['fox_sumber_air.png', 'fox_aliran_air.png', 'fox_kitaran_air.png', 'fox_aliran_semula_jadi.png', 'fox_angin.png', 'fox_udara.png', 'fox_roket_angin.png'],
    'unit10Data': ['fox_binaan_pilihan.png', 'fox_manual.png', 'fox_jurutera.png', 'fox_kreatif.png', 'fox_simpan_binaan.png']
}

for unit_name, images in images_map.items():
    # Find the array block for the unit
    pattern = rf'(const {unit_name} = \[)(.*?)(\];)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        block = match.group(2)
        new_block = ""
        # Process line by line
        lines = block.split('\n')
        for line in lines:
            if "{ type:" in line and "image:" not in line:
                img = random.choice(images)
                # Just insert the image property right after "{ type: 'xxx', "
                line = re.sub(r"({ type: '[^']+', )", rf"\g<1>image: 'images/{img}?v=2', ", line)
            new_block += line + '\n'
        
        # trim the trailing newline added by split
        new_block = new_block[:-1]
        
        # replace block in content
        content = content[:match.start(2)] + new_block + content[match.end(2):]

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js successfully!")
