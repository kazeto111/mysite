import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from briefSNS.models import Message
from django.contrib.auth import get_user_model
print("consumer.py")

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer( AsyncWebsocketConsumer ):
    print("chatConsumerクラス")

    # WebSocket接続時の処理
    async def connect( self ):
        # グループに参加
        print("def connectからです１")
        self.strGroupName = 'chat'
        #urlからグループの名前を構成
        #グループの名前を構成できるようにurlを設計する必要がある。
        #グループ化しないとdmがすべてのユーザーに受け渡れてしまう
        name1, name2 = self.scope['url_route']['kwargs']['name1'], self.scope['url_route']['kwargs']['name2']
        if name1 >= name2: self.strGroupName = name1 + name2
        else: self.strGroupName = name2 + name1
        await self.channel_layer.group_add( self.strGroupName, self.channel_name )
        print("def connectからです2")
        await self.accept()
        print("def connectからです3")

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )

    #メッセージを受け取ったらグループ内の全員(今回はDMをしている2人)に送る
    async def receive( self, text_data ):
        text_data_json = json.loads( text_data )
        await self.createMessage(text_data_json)

        # メッセージの取り出し
        strMessage = text_data_json['message']
        messangerName = text_data_json['messagengername']
        data = {
            'type': 'chat_message', 
            'message': strMessage,
            'messagengername': messangerName,
        }
        await self.channel_layer.group_send( self.strGroupName, data )

    #typeで指定された名前の関数
    async def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'messagengername':data['messagengername']
        }

        await self.send( text_data=json.dumps( data_json ) )
    
    @database_sync_to_async
    def createMessage(self, event):
        try:
            Message.objects.create(
                partner = get_user_model().objects.get(id=event['partnerpk']),
                myname = get_user_model().objects.get(id=event['userpk']),
                content=event['message']
            )
        except Exception as e:
            raise
