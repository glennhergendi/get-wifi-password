import subprocess

data = (
    subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    .decode("utf-8")
    .split("\n")
)
profiles = [i.split(":")[1][1:-1] for i in data if "All user profile" in i]

for i in profiles:
    results = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles", i, "key=clear"])
        .decode("utf-8")
        .split("\n")
    )
    results = [b.split(":")[1][1:-1] for b in results if "key content" in b]
    # jika ada kata sandi maka akan mencetak kata sandi
    try:
        print("{:<30}| {:<}".format(i, results[0]))

    # jika tidak maka akan mencetak kosong di depan kata sandi
    except IndexError:
        print("{:<30}| {:<}".format(i, ""))
