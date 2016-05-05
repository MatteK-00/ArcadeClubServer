from rest_framework import serializers
from arcadeclub.models import Utente, Magazzino, Gioco


class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ('username', 'pwd', 'device')


class GiocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gioco
        fields = ('id_gioco','upc','nome','anno','console', 'immagine')


class MagazzinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazzino
        fields = ('id_item','upc','nome','anno','console','stato','quality','prezzo_acquisto','data_acquisto','note')

class MagazzinoSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Magazzino
        fields = ('id_item','stato','quality','prezzo_acquisto','data_acquisto','note')

class UpcResponseSerializer(serializers.ModelSerializer):
    upc = serializers.CharField(required=False, allow_blank=True, max_length=100)
    nome = serializers.CharField(required=False, allow_blank=True, max_length=100)
    console = serializers.CharField(required=False, allow_blank=True, max_length=100)
    stato  = serializers.CharField(required=False, allow_blank=True, max_length=100)
    quality = serializers.CharField(required=False, allow_blank=True, max_length=100)
    prezzo_acquisto = serializers.CharField(required=False, allow_blank=True, max_length=100)
    prezzo_vendita = serializers.CharField(required=False, allow_blank=True, max_length=100)
    data_acquisto = serializers.CharField(required=False, allow_blank=True, max_length=100)
    data_vendita = serializers.CharField(required=False, allow_blank=True, max_length=100)



# class UtenteSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     pwd = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     device = serializers.CharField(required=False, allow_blank=True, max_length=100)

#     def create(self, validated_data):
#         """
#         Create and return a new `Utente` instance, given the validated data.
#         """
#         return Utente.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Utente` instance, given the validated data.
#         """
#         instance.username = validated_data.get('username', instance.username)
#         instance.pwd = validated_data.get('pwd', instance.pwd)
#         instance.device = validated_data.get('device', instance.device)
#         instance.save()
#         return instance


