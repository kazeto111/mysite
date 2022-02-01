import json
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from briefSNS.models import Message
from django.contrib.auth import get_user_model
#from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
print("consumer.py")

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer( AsyncWebsocketConsumer ):

    # WebSocket接続時の処理
    async def connect( self ):
        # グループに参加
        print("def connectからです１")
        self.strGroupName = 'chat'
        # name1, name2 = self.scope['url_route']['kwargs']['name1'], self.scope['url_route']['kwargs']['name2']
        name1, name2 = "aaa", "bbb"
        if name1 >= name2: self.strGroupName = name1 + name2
        else: self.strGroupName = name2 + name1
        await self.channel_layer.group_add( self.strGroupName, self.channel_name )
        print("def connectからです2")

        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()
        print("def connectからです3")

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive( self, text_data ):
        #このtextdataにはpartner/mynameの情報が必要
        text_data_json = json.loads( text_data )
        await self.createMessage(text_data_json)

        # メッセージの取り出し
        strMessage = text_data_json['message']
        messangerName = text_data_json['messagengername']
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message', # 受信処理関数名
            'message': strMessage, # メッセージ
            'messagengername': messangerName,
        }
        await self.channel_layer.group_send( self.strGroupName, data )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'messagengername':data['messagengername']
        }

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
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
