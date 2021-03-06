from random import randint as rand
from time import sleep

class MatchTeam:
        Substitution=0
        Team=0
        AllPass = 0
        SecsessfulPass = 0
        AllShoots = 0
        SecsessfulShoots = 0
        Save = 0
        Prossession = 0
        Goals = 0
        YellowCards=0
        RedCards=0
        def __init__(self,Team):
                self.Team=Team
                self.Substitution=3
        def addGoal(self):
                self.AllShoots+=1
                self.SecsessfulShoots+=1
                self.Goals+=1
        def addShoot(self):
                self.AllShoots+=1
        def addSecsessfilShoot(self):
                self.SecsessfulShoots+=1
                self.AllShoots+=1
        def addPass(self):
                self.AllPass+=1
        def addSecsessfulPass(self):
                self.SecsessfulPass+=1
        def addSave(self):
                self.Save+=1
        def addProssession(self):
                self.Prossession+=1
        def addYellow(self,player):
                self.YellowCards+=1
                self.Team.StartPlayers[player].YellowCard+=1
                if self.Team.StartPlayers[player].YellowCard==2:
                        self.addRed(player)
        def addRed(self,player):
                self.RedCards+=1
                self.Team.StartPlayers[player].YellowCard=0
                self.Team.StartPlayers[player].RedCard=1

def Game(Team1,Team2):
        timer = 0
        MatchTeam1=MatchTeam(Team1)
        MatchTeam2=MatchTeam(Team2)
        activeteam=MatchTeam1
        notactiveteam=MatchTeam2
        additionaltime=90
        attackpointer=0
        while timer<=180:
                time=int(timer/2)
                activeteam.addProssession()
                if time == 45 or time == 90:
                        additionaltime = rand(0, 5)
                chance = rand(0,100)
                if chance <=20:
                        player = rand(1, 10)
                        activeplayer = notactiveteam.Team.StartPlayers[player]
                        while activeplayer.RedCard==1:
                                player=rand(1, 10)
                                activeplayer = notactiveteam.Team.StartPlayers[player]
                        if rand(0,150)==75:
                                notactiveteam.addRed(player)
                        elif rand(0,100)<=10:
                                notactiveteam.addYellow(player)
                        if rand(0,200)<=2:
                                activeplayer=activeteam.Team.StartPlayers[rand(1,10)]
                                for Player in activeteam.Team.ReservePlayers:
                                        if Player.Position==activeplayer.Position and Player.IsSubstitution==0:
                                                Player.IsSubstitution=1
                                                Player,activeplayer=activeplayer,Player
                                                activeteam.Substitution-=1
                                                break
                if ((time>=60 and rand(0,100)<=5) or rand(0,200<=4)) and activeteam.Substitution==0:
                        activeplayer = activeteam.Team.StartPlayers[rand(1, 10)]
                        for Player in activeteam.Team.ReservePlayers:
                                if Player.Position == activeplayer.Position:
                                        Player.IsSubstitution = 1
                                        Player, activeplayer = activeplayer, Player
                                        activeteam.Substitution -= 1
                                        break
                if attackpointer<4:
                        chance = rand(0,100)
                        activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders,10)]
                        while activeplayer.RedCard == 1:
                                activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders, 10)]
                        if chance<activeplayer.Rating:
                                attackpointer+=1
                                activeteam.addSecsessfulPass()
                        else:
                                attackpointer=0
                                activeteam.addPass()
                                activeteam, notactiveteam = notactiveteam, activeteam
                else:
                        chance = rand(0,100)
                        if chance<=50:
                                chance = rand(0, 100)
                                activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders, 10)]
                                while activeplayer.RedCard == 1:
                                        activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders, 10)]
                                if chance < activeplayer.Rating:
                                        attackpointer += 1
                                        activeteam.addSecsessfulPass()
                                else:
                                        attackpointer=0
                                        activeteam.addPass()
                                        activeteam, notactiveteam = notactiveteam, activeteam
                        else:
                                chance = rand(0,100)
                                if chance <30:
                                        activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders,10-activeteam.Team.Strikers)]
                                        while activeplayer.RedCard == 1:
                                                activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders, 10 - activeteam.Team.Strikers)]
                                else:
                                        activeplayer = activeteam.Team.StartPlayers[rand(10 - activeteam.Team.Strikers,10)]
                                        while activeplayer.RedCard == 1:
                                                activeplayer = activeteam.Team.StartPlayers[rand(activeteam.Team.Defenders, 10 - activeteam.Team.Strikers)]
                                chance=rand(0,100)
                                if chance<=activeplayer.Rating/2:
                                        activeteam.addShoot()
                                        activeteam, notactiveteam = notactiveteam, activeteam
                                        attackpointer=0
                                elif rand(0,activeplayer.Shoot)>notactiveteam.Team.StartPlayers[0].Rating/2:
                                        activeteam.addGoal()
                                        activeteam, notactiveteam = notactiveteam, activeteam
                                        attackpointer=0

                                else:
                                        activeteam.addSecsessfilShoot()
                                        notactiveteam.addSave()
                                        activeteam, notactiveteam = notactiveteam, activeteam
                                        attackpointer=0
                timer+=1
                sleep(0)
                if time==additionaltime+45 or time==additionaltime+90:
                        timer-=additionaltime*2
                        additionaltime=90
                        if time==45:
                                pass
                        timer+=1
        activeteam.Prossession=int(activeteam.Prossession/(activeteam.Prossession+notactiveteam.Prossession)*100)
        notactiveteam.Prossession=100-activeteam.Prossession
        activeteam.AllPass*=2
        activeteam.SecsessfulPass*=2
        notactiveteam.AllPass*=2
        notactiveteam.SecsessfulPass*=2
        if activeteam.Goals>notactiveteam.Goals:
                activeteam.Team.Points+=3
                activeteam.Team.WinGames+=1
                notactiveteam.Team.LoseGames+=1
        elif notactiveteam.Goals>activeteam.Goals:
                notactiveteam.Team.Points+=3
                activeteam.Team.LoseGames+=1
                notactiveteam.Team.WinGames+=1
        else:
                activeteam.Team.Points+=1
                activeteam.Team.DrawGames+=1
                notactiveteam.Team.DrawGames+=1
                notactiveteam.Team.Points+=1
        activeteam.Team.Games+=1
        notactiveteam.Team.Games += 1

