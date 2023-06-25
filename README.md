# elc-meter-reader
Bu projede elektronik elektrik sayaçlarından belli periyotlarla alınan verileri IoT çözüm platformu olan [ThingsBoard](https://thingsboard.io/) üzerinden kullanıcılara görsel veri ve analizler gösterilmesi amaçlanmıştır.

## İçindekiler
* [elc-meter-reader](#elc-meter-reader)
  * [Hakkında](#hakkında)
  * [Gereksinimler](#gereksinimler)
  * [Kurulum](#kurulum)
  * [Usage](#usage)
  * [Contributing](#contributing)

## Hakkında
Sayaç okuma verileri Raspberry Pi üzerinde koşan SQLite3 veri tabanına kayıt edilmektedir. Üç fazlı elektronik kombi sayaçlar ve bir fazlı elektronik elektrik sayaçları için ayrı bir veri tabanı oluşturmaktadır. Hangi türden sayaç kullanılacak ise mainde sayaç türü belirtilmesi diğer modüllerin import edilmesini tetikleyecektir.

## Gereksinimler
| Derleyici | Versiyon |
| :- | :-: |
| [Python](https://www.python.org/downloads/) | `3.9+` |

| Kütüphane | Versiyon |
| :- | :-: |
| [pySerial](https://pypi.org/project/pyserial/3.5/) | `3.5` |

## Kurulum
Sadece [main.py](main.py) dosyasındaki "[METER_PHASE_TYPE](main.py#L26)" değişkenine sayaç 1 fazlı ise 1, 3 fazlı ise 3 ataması yapılması yeterlidir.
