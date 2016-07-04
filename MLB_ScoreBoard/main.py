#Imports
import xml.etree.ElementTree as ET
import urllib
import time
from graphics import *
import os.path


#Date/Time Functions
def getCurrentDate() :
    currentDate=(time.strftime("%m/%d/%Y"))
    return currentDate;
##   
def getCurrentTime() :
    currentTime=(time.strftime("%H:%M:%S"))
    return currentTime;
##
###


#MLB XML Functions
#Format URL | http://gd2.mlb.com/components/game/mlb/year_#Y/month_#M/day_#D/scoreboard.xml
def generateMLB_URL( date ) :
    month=date.split("/",1)[0]
    print "Month: " + month
    day=date.split("/",1)[1].split("/",1)[0]
    print "Day: " +  day
    year=date.split("/",1)[1].split("/",1)[1]
    print "Year: " + year
    url='http://gd2.mlb.com/components/game/mlb/year_'+year+'/month_'+month+'/day_'+"02"+'/scoreboard.xml'
    return url;
##
#Get XML
def getXML ( url ) :
    xml_str = urllib.urlopen(url).read()
    #print xml_str
    xmldoc = ET.fromstring(xml_str)
    return xmldoc;
##

def getPreGameInfo( xmldoc ) :
    print "===PreGames Info==="
    #Pregame List
    preGameList = []

    #Get games that are in PREGAME status
    game = xmldoc.findall("*/game[@status='PRE_GAME']")
    teams = xmldoc.findall("*/game[@status='PRE_GAME']/../team")
    probablePitcherName = xmldoc.findall("*/game[@status='PRE_GAME']/../p_pitcher/pitcher")
    probablePitcherStats = xmldoc.findall("*/game[@status='PRE_GAME']/../p_pitcher")
     
    print "Number of Games:",len(game)
    print "Number of Teams:",len(teams)
    #print "Number of Pitchers:",len(probablePitcherName)
    #print "Number of Pitcher Lines:",len(probablePitcherStats)
    
    
    if(len(game)!=0) :
        #Build PREGAME Info Dictionary
        for i in xrange(0,len(game)) : 
        
            gameID=game[i].attrib.get('id')
            #print "Game ID:", gameID
            teams = xmldoc.findall("*/game[@id='"+gameID+"']/../team")
            homeTeam=teams[0].attrib.get('name')
            #print "Home Team:",homeTeam
            awayTeam=teams[1].attrib.get('name')
            #print "Away Team:",awayTeam
            probablePitcherName = xmldoc.findall("*/game[@id='"+gameID+"']/../p_pitcher/pitcher")
            probablePitcherStats = xmldoc.findall("*/game[@id='"+gameID+"']/../p_pitcher")
            
            #MLB changes Pregame elements ~hour before game time
            #Check to see if they still exist
            if(len(probablePitcherName)!=0) :
                homePitcherName=probablePitcherName[0].attrib.get('name')
                homePitcherWs=probablePitcherStats[0].attrib.get('wins')
                homePitcherLs=probablePitcherStats[0].attrib.get('losses')
                homePitcherERA=probablePitcherStats[0].attrib.get('era')
                
                awayPitcherName=probablePitcherName[1].attrib.get('name')
                awayPitcherWs=probablePitcherStats[1].attrib.get('wins')
                awayPitcherLs=probablePitcherStats[1].attrib.get('losses')
                awayPitcherERA=probablePitcherStats[1].attrib.get('era')
                
                #print "Home Pitcher:",homePitcherName,"W:",homePitcherWs,"L:",homePitcherLs,"ERA:",homePitcherERA
                #print "Away Pitcher:",awayPitcherName,"W:",awayPitcherWs,"L:",awayPitcherLs,"ERA:",awayPitcherERA
                pregameInfo = {'StartTime': game[i].attrib.get('start_time'), 'H_Team': homeTeam, 'H_Pitcher': homePitcherName, 'H_Pitcher_W': homePitcherWs, 'H_Pitcher_L': homePitcherLs, 'H_Pitcher_ERA': homePitcherERA, 'A_Team': awayTeam, 'A_Pitcher': awayPitcherName, 'A_Pitcher_W': awayPitcherWs, 'A_Pitcher_L': awayPitcherLs, 'A_Pitcher_ERA': awayPitcherERA,}
                #print pregameInfo
            else :
                pregameInfo = {'StartTime': game[i].attrib.get('start_time'), 'H_Team': homeTeam, 'A_Team': awayTeam}
                #print pregameInfo
            
            ##Add to list
            preGameList.append(pregameInfo)
            
        print "List Size: ",len(preGameList)

    return preGameList;
###

def getCompletedGameInfo( xmldoc ) :
    print "===Completed Games Info==="
    #Completed List
    completedGameList = []
    
    #Get games that are in FINAL status
    game = xmldoc.findall("*/game[@status='FINAL']")
    teams = xmldoc.findall("*/game[@status='FINAL']/../team")
    winningPitcherName = xmldoc.findall("*/game[@status='FINAL']/../w_pitcher/pitcher")
    winningPitcherStats = xmldoc.findall("*/game[@status='FINAL']/../w_pitcher")
    losingPitcherName = xmldoc.findall("*/game[@status='FINAL']/../l_pitcher/pitcher")
    losingPitcherStats = xmldoc.findall("*/game[@status='FINAL']/../l_pitcher")
    savePitcherName = xmldoc.findall("*/game[@status='FINAL']/../sv_pitcher/pitcher")
    savePitcherStats = xmldoc.findall("*/game[@status='FINAL']/../sv_pitcher")
     
    print "Number of Games:",len(game)
    print "Number of Teams:",len(teams)
    
    #Build COMPLETED Info Dictionary
    for i in xrange(0,len(game)) : 
        gameID=game[i].attrib.get('id')
        #print "Game ID:", gameID
        teams = xmldoc.findall("*/game[@id='"+gameID+"']/../team")
        homeTeam=teams[0].attrib.get('name')
        #print "Home Team:",homeTeam
        awayTeam=teams[1].attrib.get('name')
        #print "Away Team:",awayTeam
        #Game Stats
        #homeTeam
        homeTeamScore = xmldoc.findall("*/game[@id='"+gameID+"']/../team[@name='"+homeTeam+"']/gameteam")
        #awayTeam
        awayTeamScore = xmldoc.findall("*/game[@id='"+gameID+"']/../team[@name='"+awayTeam+"']/gameteam")
        
        #If the home team scored more than the away team..
        if int(homeTeamScore[0].attrib.get('R')) > int(awayTeamScore[0].attrib.get('R')) :
            #print homeTeam,"won",homeTeamScore[0].attrib.get('R'),"to",awayTeamScore[0].attrib.get('R')
            winningTeamName=homeTeam
        else : 
            #print awayTeam,"won",awayTeamScore[0].attrib.get('R'),"to",homeTeamScore[0].attrib.get('R')
            winningTeamName=awayTeam
        
        #Pitchers Info
        winningPitcherName = xmldoc.findall("*/game[@id='"+gameID+"']/../w_pitcher/pitcher")
        winningPitcherStats = xmldoc.findall("*/game[@id='"+gameID+"']/../w_pitcher")
        losingPitcherName = xmldoc.findall("*/game[@id='"+gameID+"']/../l_pitcher/pitcher")
        losingPitcherStats = xmldoc.findall("*/game[@id='"+gameID+"']/../l_pitcher")
        savePitcherName = xmldoc.findall("*/game[@id='"+gameID+"']/../sv_pitcher/pitcher")
        savePitcherStats = xmldoc.findall("*/game[@id='"+gameID+"']/../sv_pitcher")
        
        #Check to see if a pitcher recorded a save
        if(savePitcherName[0].attrib.get('name')!='. ') : #Save Recorded
            
            completedInfo = {'StartTime': game[i].attrib.get('start_time'), 'W_Team': winningTeamName, 'H_Team': homeTeam, 'H_Team_Hs': homeTeamScore[0].attrib.get('H'), 'H_Team_Rs': homeTeamScore[0].attrib.get('R'), 'H_Team_Es': homeTeamScore[0].attrib.get('E'), 'A_Team': awayTeam, 'A_Team_Hs': awayTeamScore[0].attrib.get('H'), 'A_Team_Rs': awayTeamScore[0].attrib.get('R'), 'A_Team_Es': awayTeamScore[0].attrib.get('E'), 'W_Pitcher': winningPitcherName[0].attrib.get('name'), 'W_Pitcher_Ws': winningPitcherStats[0].attrib.get('wins'),'W_Pitcher_Ls': winningPitcherStats[0].attrib.get('loses'), 'L_Pitcher': losingPitcherName[0].attrib.get('name'),'L_Pitcher_Ws': losingPitcherStats[0].attrib.get('wins'),'L_Pitcher_Ls': losingPitcherStats[0].attrib.get('loses'), 'S_Pitcher': savePitcherName[0].attrib.get('name'),'S_Pitcher_Ss': savePitcherStats[0].attrib.get('saves')}
            #print completedInfo
        
        else : #Save Not Recorded
            completedInfo = {'StartTime': game[i].attrib.get('start_time'), 'W_Team': winningTeamName, 'H_Team': homeTeam, 'H_Team_Hs': homeTeamScore[0].attrib.get('H'), 'H_Team_Rs': homeTeamScore[0].attrib.get('R'), 'H_Team_Es': homeTeamScore[0].attrib.get('E'), 'A_Team': awayTeam, 'A_Team_Hs': awayTeamScore[0].attrib.get('H'), 'A_Team_Rs': awayTeamScore[0].attrib.get('R'), 'A_Team_Es': awayTeamScore[0].attrib.get('E'), 'W_Pitcher': winningPitcherName[0].attrib.get('name'), 'W_Pitcher_Ws': winningPitcherStats[0].attrib.get('wins'),'W_Pitcher_Ls': winningPitcherStats[0].attrib.get('loses'), 'L_Pitcher': losingPitcherName[0].attrib.get('name'),'L_Pitcher_Ws': losingPitcherStats[0].attrib.get('wins'),'L_Pitcher_Ls': losingPitcherStats[0].attrib.get('loses')}
            #print completedInfo


        ##Add to list
        completedGameList.append(completedInfo)
            
    print "List Size: ",len(completedGameList)
    return completedGameList;
###

def getInProgressGameInfo( xmldoc ) :
    print "===In Progress Games Info==="
    #In Progress List
    inProgressGameList = []
    
    #Get games that are in FINAL status
    game = xmldoc.findall("*/game[@status='IN_PROGRESS']")
    teams = xmldoc.findall("*/game[@status='IN_PROGRESS']/../team")
     
    print "Number of Games:",len(game)
    print "Number of Teams:",len(teams)

    if(len(game)!=0) :
        #Build IN PROGRESS Info Dictionary
        for i in xrange(0,len(game)) : 
        
            gameID=game[i].attrib.get('id')
            #print "Game ID:", gameID
            teams = xmldoc.findall("*/game[@id='"+gameID+"']/../team")
            homeTeam=teams[0].attrib.get('name')
            #print "Home Team:",homeTeam
            awayTeam=teams[1].attrib.get('name')
            #print "Away Team:",awayTeam
            #Game Stats
            #homeTeam
            homeTeamScore = xmldoc.findall("*/game[@id='"+gameID+"']/../team[@name='"+homeTeam+"']/gameteam")
            #awayTeam
            awayTeamScore = xmldoc.findall("*/game[@id='"+gameID+"']/../team[@name='"+awayTeam+"']/gameteam")
            inningNumber = xmldoc.findall("*/game[@id='"+gameID+"']/../inningnum")
            pitcher = xmldoc.findall("*/game[@id='"+gameID+"']/../pitcher")
            batter = xmldoc.findall("*/game[@id='"+gameID+"']/../batter")
            #print "Inning:",inningNumber[0].attrib.get('inning'),inningNumber[0].attrib.get('half')
            outs = xmldoc.findall("*/game[@id='"+gameID+"']/..")
            #print "Outs:",outs[0].attrib.get('outs')
            #print "Pitcher:",pitcher[0].attrib.get('name')
            #print "Batter:",batter[0].attrib.get('name')

            #Get Base Runners
            firstBaseRunner = xmldoc.findall("*/game[@id='"+gameID+"']/../on_base[@base='1']/player")
            #print firstBaseRunner[0].attrib.get('name')
            secondBaseRunner = xmldoc.findall("*/game[@id='"+gameID+"']/../on_base[@base='2']/player")
            #print secondBaseRunner[0].attrib.get('name')
            thirdBaseRunner = xmldoc.findall("*/game[@id='"+gameID+"']/../on_base[@base='3']/player")
            #print thirdBaseRunner[0].attrib.get('name')
            
            inProgressInfo = {'StartTime': game[i].attrib.get('start_time'),'Inning_Num': inningNumber[0].attrib.get('inning'), 'Inning_Half': inningNumber[0].attrib.get('half'), 'Outs': outs[0].attrib.get('outs'),'H_Team': homeTeam, 'H_Team_Hs': homeTeamScore[0].attrib.get('H'), 'H_Team_Rs': homeTeamScore[0].attrib.get('R'), 'H_Team_Es': homeTeamScore[0].attrib.get('E'), 'A_Team': awayTeam, 'A_Team_Hs': awayTeamScore[0].attrib.get('H'), 'A_Team_Rs': awayTeamScore[0].attrib.get('R'), 'A_Team_Es': awayTeamScore[0].attrib.get('E')}
            
            #Check if runner is on first base.. If so add to dictionary
            if(len(firstBaseRunner)!=0) :
                inProgressInfo['firstBaseRunner'] = firstBaseRunner[0].attrib.get('name')
                
            #Check if runner is on second base.. If so add to dictionary
            if(len(secondBaseRunner)!=0) :
                inProgressInfo['secondBaseRunner'] = secondBaseRunner[0].attrib.get('name')
            
            #Check if runner is on third base.. If so add to dictionary
            if(len(thirdBaseRunner)!=0) :
                inProgressInfo['thirdBaseRunner'] = thirdBaseRunner[0].attrib.get('name')
            
            #print inProgressInfo
            
            inProgressGameList.append(inProgressInfo)
    print "List Size: ",len(inProgressGameList)        
    return inProgressGameList;
###

def graphics( listInfo ) :
    num_games=15

    win = GraphWin('Scoreboard', 2000, 1500) # give title and dimensions

    #Case: 15 Games
    if(num_games==15):
        gameIndex=0
        row=0
        column=0
        square_width=300
        square_height=300
        while column < num_games/5:
            row=0
            while row < num_games/3:
                #square
                square = Rectangle(Point((row+1)*square_width,(column+1)*square_height),Point(row*square_width,column*square_height))
                
                if(column%2==0): 
                    if(row%2==0): 
                        square.setFill('#397D02')
                        print "1"
                    else:
                        square.setFill('#567E3A')
                        print "2"
                else:
                    if(row%2==1): 
                        square.setFill('#397D02')
                        print "1"
                    else:
                        square.setFill('#567E3A')
                        print "2"
                square.draw(win)
                
                #diamond
                diamondX=((row*square_width)+((row+1)*square_width))/2
                diamondY=(125+(column*square_width))##Fix this to multiple
                diamond = Image(Point(diamondX,diamondY), "rsz_diamond.png")
                diamond.draw(win)
                
                ##away team info
                #away team logo
                awayTeamLogo_fileName=getTeamAbbreviation(listInfo[gameIndex].get('A_Team'))+".png"
                
                #Check if team has logo
                if os.path.isfile("/home/john_riley/Desktop/MLB_ScoreBoard/Team_Logos/"+awayTeamLogo_fileName):
                    awayTeamLogoX=((row*square_width)+60)
                    awayTeamLogoY=(((column+1)*square_height)-240)
                
                    awayTeam_logo = Image(Point(awayTeamLogoX,awayTeamLogoY),"Team_Logos/"+awayTeamLogo_fileName)
                    awayTeam_logo.draw(win)
                    
                ##away team score color
                #stats color (white)
                awayTeamNameColorX1=((row*square_width))
                awayTeamNameColorX2=((row+1)*square_height)-160
                awayTeamNameColorY1=(((column+1)*square_height)-60)
                awayTeamNameColorY2=(((column+1)*square_height))
                rectangle = Rectangle(Point(awayTeamNameColorX1,awayTeamNameColorY1),Point(awayTeamNameColorX2,awayTeamNameColorY2))
                rectangle.setFill('#ffffff')
                rectangle.draw(win)
                
                #away team color
                awayTeamNameColorX1=((row*square_width))
                awayTeamNameColorX2=((row+1)*square_height)-240
                awayTeamNameColorY1=(((column+1)*square_height)-60)
                awayTeamNameColorY2=(((column+1)*square_height)-30)
                rectangle = Rectangle(Point(awayTeamNameColorX1,awayTeamNameColorY1),Point(awayTeamNameColorX2,awayTeamNameColorY2))
                rectangle.setFill(getTeamPrimaryColor(listInfo[gameIndex].get('A_Team')))
                rectangle.draw(win)
                    
                #away team name
                awayTeamNameTextX=((row*square_width)+30)
                awayTeamNameTextY=(((column+1)*square_height)-45)
                awayTeamName_text = Text(Point(awayTeamNameTextX,awayTeamNameTextY),getTeamAbbreviation(listInfo[gameIndex].get('A_Team')))
                awayTeamName_text.setFill(getTeamSecondaryColor(listInfo[gameIndex].get('A_Team')))
                awayTeamName_text.draw(win)
                
                #away team runs
                awayTeamRunsTextX=((row*square_width)+70)
                awayTeamRunsTextY=(((column+1)*square_height)-45)
                awayTeamRuns_text = Text(Point(awayTeamRunsTextX,awayTeamRunsTextY),listInfo[gameIndex].get('A_Team_Rs'))
                awayTeamRuns_text.draw(win)
                
                #away team hits
                awayTeamHitsTextX=((row*square_width)+100)
                awayTeamHitsTextY=(((column+1)*square_height)-45)
                awayTeamHits_text = Text(Point(awayTeamHitsTextX,awayTeamHitsTextY),listInfo[gameIndex].get('A_Team_Hs'))
                awayTeamHits_text.draw(win)
                
                #away team errors
                awayTeamErrorsTextX=((row*square_width)+130)
                awayTeamErrorsTextY=(((column+1)*square_height)-45)
                awayTeamErrors_text = Text(Point(awayTeamErrorsTextX,awayTeamErrorsTextY),listInfo[gameIndex].get('A_Team_Es'))
                awayTeamErrors_text.draw(win)
                
                ##home team info
                #home team logo
                homeTeamLogo_fileName=getTeamAbbreviation(listInfo[gameIndex].get('H_Team'))+".png"
                
                #Check if team has logo
                if os.path.isfile("/home/john_riley/Desktop/MLB_ScoreBoard/Team_Logos/"+homeTeamLogo_fileName):
                    homeTeamLogoX=((row*square_width)+240)
                    homeTeamLogoY=(((column+1)*square_height)-240)
                
                    homeTeam_logo = Image(Point(homeTeamLogoX,homeTeamLogoY),"Team_Logos/"+homeTeamLogo_fileName)
                    homeTeam_logo.draw(win)
                    
                ##home team score color
                #stats color (white)
                homeTeamNameColorX1=((row*square_width))
                homeTeamNameColorX2=((row+1)*square_height)-160
                homeTeamNameColorY1=(((column+1)*square_height)-30)
                homeTeamNameColorY2=(((column+1)*square_height))
                rectangle = Rectangle(Point(homeTeamNameColorX1,homeTeamNameColorY1),Point(homeTeamNameColorX2,homeTeamNameColorY2))
                rectangle.setFill('#ffffff')
                rectangle.draw(win)
                
                #home team color
                homeTeamNameColorX1=((row*square_width))
                homeTeamNameColorX2=((row+1)*square_height)-240
                homeTeamNameColorY1=(((column+1)*square_height)-30)
                homeTeamNameColorY2=(((column+1)*square_height))
                rectangle = Rectangle(Point(homeTeamNameColorX1,homeTeamNameColorY1),Point(homeTeamNameColorX2,homeTeamNameColorY2))
                rectangle.setFill(getTeamPrimaryColor(listInfo[gameIndex].get('H_Team')))
                rectangle.draw(win)
                     
                #home team name
                homeTeamNameTextX=((row*square_width)+30)
                homeTeamNameTextY=(((column+1)*square_height)-15)
                homeTeamName_text = Text(Point(homeTeamNameTextX,homeTeamNameTextY),getTeamAbbreviation(listInfo[gameIndex].get('H_Team')))
                homeTeamName_text.setFill(getTeamSecondaryColor(listInfo[gameIndex].get('H_Team')))
                homeTeamName_text.draw(win)
                
                #home team runs
                homeTeamRunsTextX=((row*square_width)+70)
                homeTeamRunsTextY=(((column+1)*square_height)-15)
                homeTeamRuns_text = Text(Point(homeTeamRunsTextX,homeTeamRunsTextY),listInfo[gameIndex].get('H_Team_Rs'))
                homeTeamRuns_text.draw(win)
                
                #home team hits
                homeTeamHitsTextX=((row*square_width)+100)
                homeTeamHitsTextY=(((column+1)*square_height)-15)
                homeTeamHits_text = Text(Point(homeTeamHitsTextX,homeTeamHitsTextY),listInfo[gameIndex].get('H_Team_Hs'))
                homeTeamHits_text.draw(win)
                
                #home team errors
                homeTeamErrorsTextX=((row*square_width)+130)
                homeTeamErrorsTextY=(((column+1)*square_height)-15)
                homeTeamErrors_text = Text(Point(homeTeamErrorsTextX,homeTeamErrorsTextY),listInfo[gameIndex].get('H_Team_Es'))
                homeTeamErrors_text.draw(win)

                gameIndex = gameIndex + 1
                row = row + 1
            column = column + 1


    win.getMouse()
    win.close()


    return;
###

def getTeamAbbreviation( teamName ):
    #return team abbreviation
    if(teamName=="Angels"):
        return "LAA";
    if(teamName=="Astros"):
        return "HOU";
    if(teamName=="Athletics"):
        return "OAK";
    if(teamName=="Blue Jays"):
        return "TOR";
    if(teamName=="Braves"):
        return "ATL";
    if(teamName=="Brewers"):
        return "MIL";
    if(teamName=="Cardinals"):
        return "STL";
    if(teamName=="Cubs"):
        return "CHC";
    if(teamName=="D-backs"):
        return "ARI";      
    if(teamName=="Dodgers"):
        return "LAD";
    if(teamName=="Giants"):
        return "SF";
    if(teamName=="Indians"):
        return "CLE";
    if(teamName=="Mariners"):
        return "SEA";
    if(teamName=="Marlins"):
        return "MIA";
    if(teamName=="Mets"):
        return "NYM";
    if(teamName=="Nationals"):
        return "WSH";
    if(teamName=="Orioles"):
        return "BAL";
    if(teamName=="Padres"):
        return "SD";    
    if(teamName=="Phillies"):
        return "PHI";
    if(teamName=="Pirates"):
        return "PIT";
    if(teamName=="Rangers"):
        return "TEX";
    if(teamName=="Rays"):
        return "TBR";
    if(teamName=="Red Sox"):
        return "BOS";
    if(teamName=="Reds"):
        return "CIN";
    if(teamName=="Rockies"):
        return "COL";
    if(teamName=="Royals"):
        return "KC";
    if(teamName=="Tigers"):
        return "DET";
    if(teamName=="Twins"):
        return "MIN";
    if(teamName=="White Sox"):
        return "CHW";
    if(teamName=="Yankees"):
        return "NYY";
        
    return "Unknown" #Default Error
###

def getTeamPrimaryColor( teamName ):
    #return team color
    if(teamName=="Angels"):
        return "#BA0021";
    if(teamName=="Astros"):
        return "#EB6E1F";
    if(teamName=="Athletics"):
        return "#003831";
    if(teamName=="Blue Jays"):
        return "#134A8E";
    if(teamName=="Braves"):
        return "#13274F";
    if(teamName=="Brewers"):
        return "#0A2351";
    if(teamName=="Cardinals"):
        return "#C41E3A";
    if(teamName=="Cubs"):
        return "#0E3386";
    if(teamName=="D-backs"):
        return "#A71930";      
    if(teamName=="Dodgers"):
        return "#005A9C";
    if(teamName=="Giants"):
        return "#FD5A1E";
    if(teamName=="Indians"):
        return "#002B5C";
    if(teamName=="Mariners"):
        return "#005C5C";
    if(teamName=="Marlins"):
        return "#FF6600";
    if(teamName=="Mets"):
        return "#002D72";
    if(teamName=="Nationals"):
        return "#AB0003";
    if(teamName=="Orioles"):
        return "#DF4601";
    if(teamName=="Padres"):
        return "#002D62";    
    if(teamName=="Phillies"):
        return "#E81828";
    if(teamName=="Pirates"):
        return "#FDB827";
    if(teamName=="Rangers"):
        return "#C0111F";
    if(teamName=="Rays"):
        return "#8FBCE6";
    if(teamName=="Red Sox"):
        return "#BD3039";
    if(teamName=="Reds"):
        return "#C6011F";
    if(teamName=="Rockies"):
        return "#333366";
    if(teamName=="Royals"):
        return "#004687";
    if(teamName=="Tigers"):
        return "#0C2C56";
    if(teamName=="Twins"):
        return "#002B5C";
    if(teamName=="White Sox"):
        return "#C4CED4";
    if(teamName=="Yankees"):
        return "#003087";

    return "#000000" #Default Error
###

def getTeamSecondaryColor( teamName ):
    #return team color
    if(teamName=="Angels"):
        return "#003263";
    if(teamName=="Astros"):
        return "#002D62";
    if(teamName=="Athletics"):
        return "#EFB21E";
    if(teamName=="Blue Jays"):
        return "#E8291C";
    if(teamName=="Braves"):
        return "#CE1141";
    if(teamName=="Brewers"):
        return "#B6922E";
    if(teamName=="Cardinals"):
        return "#FEDB00";
    if(teamName=="Cubs"):
        return "#CC3433";
    if(teamName=="D-backs"):
        return "#E3D4AD";      
    if(teamName=="Dodgers"):
        return "#EF3E42";
    if(teamName=="Giants"):
        return "#000000";
    if(teamName=="Indians"):
        return "#E31937";
    if(teamName=="Mariners"):
        return "#0C2C56";
    if(teamName=="Marlins"):
        return "#0077C8";
    if(teamName=="Mets"):
        return "#FF5910";
    if(teamName=="Nationals"):
        return "#11225B";
    if(teamName=="Orioles"):
        return "#000000";
    if(teamName=="Padres"):
        return "#FEC325";    
    if(teamName=="Phillies"):
        return "#284898";
    if(teamName=="Pirates"):
        return "#000000";
    if(teamName=="Rangers"):
        return "#003278";
    if(teamName=="Rays"):
        return "#092C5C";
    if(teamName=="Red Sox"):
        return "#0D2B56";
    if(teamName=="Reds"):
        return "#000000";
    if(teamName=="Rockies"):
        return "#C4CED4";
    if(teamName=="Royals"):
        return "#C09A5B";
    if(teamName=="Tigers"):
        return "#E66A20";
    if(teamName=="Twins"):
        return "#D31145";
    if(teamName=="White Sox"):
        return "#000000";
    if(teamName=="Yankees"):
        return "#E4002B";

    return "#000000" #Default Error
###
    
####








    
    
    
    
#Testing..    
print "Date: " + getCurrentDate()
print "Time: " + getCurrentTime()
print generateMLB_URL( getCurrentDate() )
testXML = getXML( generateMLB_URL( getCurrentDate() ) )
getPreGameInfo( testXML )
testList = getCompletedGameInfo( testXML )
getInProgressGameInfo( testXML )
graphics( testList )
