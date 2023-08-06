from core import ShadowUserAgent

shadow_useragent = ShadowUserAgent()

print(shadow_useragent.firefox)
print(shadow_useragent.chrome)
print(shadow_useragent.safari)
print(shadow_useragent.edge)
print(shadow_useragent.ie)
print(shadow_useragent.android)
print(shadow_useragent.ipad)
print(shadow_useragent.random)
print(shadow_useragent.random_nomobile)
uu = shadow_useragent.get_sorted_uas()
shadow_useragent.force_update()
for u in uu:
    print(u)

