class NetworkPlayer(Player):
    def __init__(self, xy):
        Player.__init__(self, xy)

    def tick(self, socket, level, delta):
        #Get data
    
        Tank.tick(self, level, delta)

    def setX(self, x):
        self.circle[0] = round(x)
        
    def setY(self, y):
        self.circle[1] = round(y)

    def destroy(self):
        Tank.destroy(self)
