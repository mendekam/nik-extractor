import ocr as model

class Router:
    @staticmethod
    def run(app):
        @app.route('/')
        def home():
            return {
                'message':'NIP Extractor API',
            }

        @app.route('/api/extract_nik', methods=['POST'])
        def extract_nik():
            return model.extract_nik()
        
        @app.route('/api/extract_nip', methods=['POST'])
        def extract_nip():
            return model.extract_nip()
        