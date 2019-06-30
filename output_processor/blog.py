from os.path import join

from fpdf import FPDF

from output_processor import ScrapperOutputProcessor

class BlogEntryOutputProcessor(ScrapperOutputProcessor):
    content = 'blog'
    def build_pdf(self, directory, blog_data):
        header = blog_data.header
        contents = blog_data.contents
        
        pdf_path = join(directory, f"{header.title}.pdf")
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        pdf.add_font('fireflysung', '', 'fireflysung.ttf', uni=True) 
        pdf.set_font('fireflysung', '', 14)
        
        for content in contents:
            print(content)
            # pdf.write(8, content.get_content())
            # pdf.ln(8)
            # pdf.cell(0, 0, txt='TEST', ln=1)
        
        pdf.output(pdf_path)

    def process_blog_data(self, blog_datas):
        directory = self.output_folder_handler.get_directory_for_member_subdirectories(self.content)
        for blog_data in blog_datas:
            self.build_pdf(directory, blog_data)
