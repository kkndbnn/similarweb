
def replacement(file_write, file_read):
    with open(file_write, "w") as f:
        with open(file_read, "r") as file:
            r = file.read().split("}{")
            f.write(r[0][1:])
            for i in r[0:-1]:
                f.write(i + "\n")
            f.write(r[-1][:-2])

def replacement_json(file_write, file_read):
    with open(file_write, "w") as for_wtite:
        with open(file_read, "r") as for_read:
            r = for_read.read()
            for_wtite.write(r)