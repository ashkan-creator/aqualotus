#!/usr/bin/env python3
"""
اسکریپت هدر v21 — برگردوندن محتوای حذف‌شده‌ی منوی همبرگر (سایدبار موبایل)
جمنای این موارد رو حذف کرده بود: «شناور»، «خانواده‌های گیاهی»، «نوع کشت»،
«نیاز به بستر»، بخش «لوازم و مکمل»، «درباره ما».
این اسکریپت کل بلوک محتوای سایدبار رو با نسخه‌ی کامل جایگزین می‌کنه.
"""
import os
import shutil

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-v21-backup")

START_MARKER = "<div style={{ padding: '8px 0' }}>"
END_MARKER = "</div>\n        </div>\n      </div>\n    </header>"

NEW_INNER = """
            <SectionLabel>\U0001F33F گیاهان زنده</SectionLabel>
            <DrawerItem icon='\U0001F331' label='همه گیاهان' onClick={() => goToFilter({ category: 'گیاهزنده' })} />

            <DrawerSection icon='\U0001F4CD' label='محل کاشت' color='#0d4f8b' isOpen={openSection === 'pos'} onToggle={() => toggleSection('pos')}>
              <SubItem label='جلو آکواریوم' onClick={() => goToFilter({ position: 'جلو' })} />
              <SubItem label='میانه آکواریوم' onClick={() => goToFilter({ position: 'میانه' })} />
              <SubItem label='پشت آکواریوم' onClick={() => goToFilter({ position: 'پشت' })} />
              <SubItem label='شناور' onClick={() => goToFilter({ position: 'شناور' })} />
            </DrawerSection>

            <DrawerSection icon='\U0001F33F' label='خانواده\u200cهای گیاهی' color='#6a1b9a' isOpen={openSection === 'fam'} onToggle={() => toggleSection('fam')}>
              {families?.map((f) => (
                <SubItem key={f._id} label={f.name} onClick={() => goToFilter({ keyword: f.name })} />
              ))}
            </DrawerSection>

            <DrawerSection icon='\U0001F4A7' label='نوع کشت' color='#006064' isOpen={openSection === 'cult'} onToggle={() => toggleSection('cult')}>
              <SubItem label='\U0001F4A7 کشت آبزی' onClick={() => goToFilter({ cultivationType: 'آبزی' })} />
              <SubItem label='\U0001F331 کشت هیدروپونیک' onClick={() => goToFilter({ cultivationType: 'هیدروپونیک' })} />
              <SubItem label='\u2705 هر دو نوع کشت' onClick={() => goToFilter({ cultivationType: 'هردو' })} />
            </DrawerSection>

            <DrawerSection icon='\U0001FAA8' label='نیاز به بستر' color='#4e342e' isOpen={openSection ==='soil'} onToggle={() => toggleSection('soil')}>
              <SubItem label='\U0001FAA8 نیاز به بستر دارد' onClick={() => goToFilter({ needsSoil: 'true'})} />
              <SubItem label='\U0001F6AB بدون نیاز به بستر' onClick={() => goToFilter({ needsSoil: 'false' })} />
            </DrawerSection>

            <Divider />
            <SectionLabel>\U0001F6D2 لوازم و مکمل</SectionLabel>
            <DrawerItem icon='\U0001F9EA' label='کود و مکمل' onClick={() => goToFilter({ category: 'کود و مکمل' })} />
            <DrawerItem icon='\U0001FAB8' label='بستر آکواریوم' onClick={() => goToFilter({ category: 'بستر' })} />
            <DrawerItem icon='\U0001F527' label='لوازم جانبی' onClick={() => goToFilter({ category: 'لوازم جانبی' })} />

            <Divider />
            <DrawerItem icon='\U0001F4D6' label='وبلاگ' onClick={() => goTo('/blog')} />
            <DrawerItem icon='\U0001F4DE' label='تماس با ما' onClick={() => goTo('/contact')} />
            <DrawerItem icon='\u2139\uFE0F' label='درباره ما' onClick={() => goTo('/about')} />
          """


def main():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "خانواده\u200cهای گیاهی" in content:
        print("✗ به‌نظر می‌رسه این بخش قبلاً برگردونده شده (خانواده‌های گیاهی پیدا شد). چیزی تغییر نکرد.")
        return

    start_idx = content.find(START_MARKER)
    if start_idx == -1:
        print("✗ انکر شروع پیدا نشد — دست نخورد.")
        return
    inner_start = start_idx + len(START_MARKER)

    end_idx = content.find(END_MARKER, inner_start)
    if end_idx == -1:
        print("✗ انکر پایان پیدا نشد — دست نخورد. ساختار Header.jsx احتمالاً فرق داره.")
        return

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {HEADER_BACKUP}")

    content = content[:inner_start] + NEW_INNER + content[end_idx:]

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ محتوای کامل سایدبار (خانواده‌ها، نوع کشت، نیاز به بستر، لوازم و مکمل، درباره ما، شناور) برگردونده شد")
    print(f"✓ فایل ذخیره شد: {HEADER_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
