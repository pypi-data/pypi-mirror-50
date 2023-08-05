from __future__ import unicode_literals

if __name__ == "__main__":
    raise

class Channel:
    OtherProps = {}

    def __init__(self, data):
        data["class"] = "channel"

        for x in data:
            if type(data[x]) != dict:
                self.OtherProps[x] = data[x]
                continue

            for y in data[x]:
                setattr(self, y, data[x][y])
