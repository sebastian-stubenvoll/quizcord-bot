import discord

class Question:
    def __init__(self, data):
        question = data[0]
        quiz = data[1]
        cC = data[2][0]
        cQ = data[2][1]

        footer = str(quiz['Title'])
        try:
            if quiz['Description'] != None:
                footer += ' – {}'.format(str(quiz['Description']))
        except KeyError:
            pass
        title = str(quiz['Categories'][cC]['Name'])
        try:
            desc = str(quiz['Categories'][cC]['Description'])
            desc = str(desc) if desc != 'None' else '\u200B'
        except KeyError:
            desc = '\u200B'

        prompt = str(question['Prompt'])
        try:
            if isinstance(question['Info'], list):
                info = ', '.join(question['Info'])
            else:
                info = str(question['Info'])
                info = '\u200B' if info == 'None' else info
        except KeyError:
            info = '\u200B'
        try:
            media = str(question['Media'])
            media = None if media == 'None' else media
        except KeyError:
            media = None
        self.media = media

        pprompt, pnts = self.pointsPrompt(question)
        points = 'worth {} points'.format(pnts)

        embed = discord.Embed(title=title, description=desc)
        embed.add_field(name=prompt, value=info, inline=False)
        embed.add_field(name=points, value=pprompt, inline=False)
        embed.set_footer(text=footer)
        self.embed = embed


    def pointsPrompt(self, question):
        qType = question['Type']
        maxPoints = str(question['Points'])
        prompt = ''
        if qType == 'Any':
            prompt = 'full point(s) for any correct answer'
        if qType == 'Exact':
            prompt = 'point(s) for the exact answer only'
        if qType == 'Each':
            maxPoints = len(question['Answer']) * question['Points']
            prompt = '{} point(s) for each correct answer. \n\
Wrong answers lose you a point though!'.format(str(question['Points']))
        if qType == 'All':
            prompt = 'full point(s) if all listing all correct answers only'

        return prompt, str(maxPoints)


    def generate(self):
        return (self.embed, self.media)


class Standings:

    def __init__(self, standings, quizdata):
        self.q = quizdata
        sortkey = lambda i: i[1]
        self.sortedStandings = dict(sorted(standings.items(), key=sortkey, reverse=True))


    def generate(self):
        embed = discord.Embed(title='Current top players', desc='')
        if not self.sortedStandings:
            embed.add_field(name='Oh no!', value='Noone\'s scored any points yet.')

        else:
            i = 1
            rank = -1
            last_v = -1
            for k, v in self.sortedStandings.items():
                rank = i if v != last_v else rank
                last_v = v
                embed.add_field(name=f'{rank}. {k}', value=f'with {v} point(s)')
                i += 1
                if i == 6:
                    break

        footer = str(self.q['Title'])
        try:
            if self.q['Description'] != None:
                footer += ' – {}'.format(str(self.q['Description']))
        except KeyError:
            pass

        embed.set_footer(text=footer)
        return embed

















