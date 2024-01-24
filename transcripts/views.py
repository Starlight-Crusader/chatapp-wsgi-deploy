from rest_framework import views, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib

from .serializers import EncDecSerializer


class EncDecView():
    def generate_iv(self, key_bytes):
        return hashlib.sha256(key_bytes).digest()[:16]


class EncryptTranscriptView(views.APIView, EncDecView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = EncDecSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        key = serializer.validated_data['key']
        text = serializer.validated_data['text']

        # Step 1: Evaluate digital fingerprint hash and concatenate to the message
        fingerprint_src_bytes = f"{key}|{text}".encode('utf-8')
        fingerprint_bytes = hashlib.sha256(fingerprint_src_bytes).digest()
        
        cryptogram_src_str = f"{base64.b64encode(fingerprint_bytes).decode()}|{text}"
        cryptogram_src_bytes = cryptogram_src_str.encode('utf-8')

        # Step 2: Hash the key to expand it to 256 bits
        actual_key_bytes = hashlib.sha3_256(key.encode('utf-8')).digest()

        # Step 3: Genearet an IV for AES
        iv = self.generate_iv(hashlib.sha256(key.encode('utf-8')).digest())

        # Step 4: Encrypt the concatenated message with AES
        ciphertext_bytes = self.encrypt_message(cryptogram_src_bytes, actual_key_bytes, iv)

        return response.Response(
            {'encrypted': base64.b64encode(ciphertext_bytes).decode()},
            status=status.HTTP_200_OK,
        )
    
    def encrypt_message(self, msg_bytes, key_bytes, iv):
        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext_bytes = encryptor.update(msg_bytes) + encryptor.finalize()

        return ciphertext_bytes
    

class DecryptTranscriptView(views.APIView, EncDecView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = EncDecSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        key = serializer.validated_data['key']
        text = serializer.validated_data['text']

        # Step 1: Hash the key to expand it to 256 bits
        actual_key_bytes = hashlib.sha3_256(key.encode('utf-8')).digest()

        # Step 2: Genearet an IV for AES
        iv = self.generate_iv(hashlib.sha256(key.encode('utf-8')).digest())

        # Step 3: Decrypt the concatenated string
        decrypted_bytes = self.decrypt_message(base64.b64decode(text), actual_key_bytes, iv)

        try:
            decrypted_message_str = decrypted_bytes.decode()

            # Step 4: Check the fingerprint
            split = decrypted_message_str.split('|')
            fingerprint_src_bytes = f"{key}|{split[1]}".encode('utf-8')
            fingerprint_bytes = hashlib.sha256(fingerprint_src_bytes).digest()

            if fingerprint_bytes != base64.b64decode(split[0]):
                return response.Response(
                    {'message': "Invalid key!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return response.Response(
                {'message': "Invalid key!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(
            {'decrypted': split[1]},
            status=status.HTTP_200_OK,
        )

    def decrypt_message(self, ciphertext_bytes, key_bytes, iv):
        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        original_text_bytes = decryptor.update(ciphertext_bytes) + decryptor.finalize()

        return original_text_bytes
