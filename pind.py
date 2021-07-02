import json
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

font = ImageFont.truetype("font/SourceHanSans.ttc", 32)


class CmNode:
    def __init__(self, parent=None):
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.parent = parent
        self.style = ""
        self.text = ""
        self.img = ""
        self.child = []

        self.gapWidth = 25
        self.gapHeight = 20

        self.renderX = 0
        self.renderY = 0

        self.renderHeight = 0
        self.renderWidth = 0

    def adjust(self, n):
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.renderX = 0
        self.renderY = 0
        self.renderHeight = 0
        self.renderWidth = 0
        if self.parent:
            self.renderX = self.parent.renderX + self.parent.w+self.parent.gapWidth
            self.renderY = self.parent.renderY + self.parent.renderHeight
            self.renderHeight = self.parent.gapHeight

        size = font.getsize(self.text)
        self.w = int(size[0] * 1.2) + 1
        self.h = int(size[1] * 1.2) + 1
        self.x = self.renderX

        self.renderWidth = self.w + self.gapWidth
        for i in range(len(self.child)):
            c = self.child[i]
            c.adjust(i)
            self.renderHeight += c.renderHeight
            self.renderWidth = max(self.renderWidth, self.w + self.gapWidth + c.renderWidth)
        if self.renderHeight < self.h+self.gapHeight:
            self.renderHeight = self.h+self.gapHeight
        if self.child:
            self.y = self.renderY + self.renderHeight//3
        else:
            self.y = self.renderY

        if not self.parent:
            self.renderY = 30
            self.renderHeight += 30

    def getDict(self):
        copy = CmNode()
        copy.x = self.x
        copy.y = self.y
        copy.w = self.w
        copy.h = self.h
        copy.parent = None
        copy.style = self.style
        copy.text = self.text
        copy.img = self.img
        copy.child = [c.getDict() for c in self.child]
        return copy.__dict__

    def print(self, n=0):
        if self.child:
            return "  " * n + ' - ' + self.text + '\n' + '\n'.join([c.print(n + 1) for c in self.child])
        return "  " * n + ' - ' + self.text

    def render(self, img):
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 173, 0), 2)
        if self.parent:
            cv2.line(img, (self.parent.x + self.parent.w, self.parent.y+self.parent.h//2), (self.x, self.y+self.h//2),
                     (134, 232, 123))
        try:
            img_pil = Image.fromarray(img[self.y:self.y + self.h, self.x:self.x + self.w])
        except ValueError:
            return
        draw = ImageDraw.Draw(img_pil)
        draw.text((2, 0), self.text, font=font, fill=(255, 255, 0))
        img2 = np.array(img_pil)
        img[self.y:self.y + self.h, self.x:self.x + self.w] = img2[0:self.h, 0:self.w]
        if self.child:
            for c in self.child:
                c.render(img)

    def copy(self, parent=None):
        ccopy = CmNode()
        ccopy.text = self.text
        ccopy.parent = parent
        ccopy.child = []
        for c in self.child:
            ccopy.child.append(c.copy(ccopy))
        return ccopy


class CmMind:
    def __init__(self):
        self.root = CmNode()


mMind = CmMind()

mMind.root.y = 30

cMind = mMind.root


def createNode(args):
    global cMind
    c_child = CmNode(cMind)
    cMind.child.append(c_child)
    cMind = c_child
    if len(args) > 0:
        setText(args)


def createButNotEnter(args):
    global cMind
    c_child = CmNode(cMind)
    cMind.child.append(c_child)
    cMind = c_child
    if len(args) > 0:
        setText(args)
    backToParent(args)


def setText(args):
    global cMind
    cMind.text = " ".join(args)


def backToParent(args):
    global cMind
    if cMind.parent:
        cMind = cMind.parent


def nextChild(args):
    global cMind
    try:
        cMind = cMind.parent.child[cMind.parent.child.index(cMind) + 1]
    except IndexError:
        cMind = cMind.parent.child[0]


def getChild(args):
    global cMind
    if len(args) == 0:
        if len(cMind.child) > 0:
            cMind = cMind.child[0]
        else:
            print("No child")


def deleteSelf(args):
    global cMind
    if not cMind.parent:
        return
    c_child = cMind
    cMind = c_child.parent
    cMind.child.remove(c_child)
    del c_child


def printTree(args):
    global mMind
    print(json.dumps(mMind.root.getDict()))


def showTree(args):
    global mMind
    print(mMind.root.print())


def listChild(args):
    global cMind
    print('\t'.join([c.text for c in cMind.child]))


def renderMap(args):
    global mMind
    mMind.root.adjust(0)
    img = np.zeros((mMind.root.renderHeight, mMind.root.renderWidth, 3), np.uint8)
    mMind.root.render(img)
    cv2.imshow(mMind.root.text, img)
    cv2.waitKey()


clip_mind = None


def copyChild(args):
    global cMind, clip_mind
    clip_mind = cMind.copy()


def cutChild(args):
    copyChild(args)
    deleteSelf(args)


def pasteChild(args):
    global cMind, clip_mind
    if clip_mind:
        cp_mind = clip_mind.copy()
        cp_mind.parent = cMind
        cMind.child.append(cp_mind)


def saveMap(args):
    global mMind
    if len(args) == 1:
        mMind.root.adjust(0)
        img = np.zeros((mMind.root.renderHeight, mMind.root.renderWidth, 3), np.uint8)
        mMind.root.render(img)
        cv2.imwrite(args[0]+".jpg", img)


def saveText(args):
    if len(args) == 1:
        file = open(args[0]+".json", 'w+')
        file.write(json.dumps(mMind.root.getDict()))
        file.close()


dctCommands = {
    'c': createNode,
    't': setText,
    's': showTree,
    'n': nextChild,
    'p': printTree,
    'b': backToParent,
    'd': deleteSelf,
    'g': getChild,
    'l': listChild,
    'q': renderMap,
    'cc': createButNotEnter,
    'x': cutChild,
    'pp': pasteChild,
    'cp': copyChild,
    'qw': saveMap,
    'qs': saveText
}


def keyProcess(args):
    if not args:
        return
    try:
        dctCommands[args[0]](args[1:])
    except KeyError:
        print("No such command.")


if __name__ == '__main__':
    while True:
        s_str = ""
        c_mind = cMind
        while c_mind:
            s_str = c_mind.text + "/" + s_str
            c_mind = c_mind.parent
        print(s_str, end=' $ ')
        _in = input()
        keyProcess(_in.split())
