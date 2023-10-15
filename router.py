import ocr as model

class Router:
    @staticmethod
    def run(app):
        @app.route('/')
        def home():
            return {
                'message':'NIP Extractor API',
            }

        @app.route('/api/extract_nip', methods=['POST'])
        def extract():
            return model.extract_nip()