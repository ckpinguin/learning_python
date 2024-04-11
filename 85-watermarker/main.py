from tkinter import Tk, Label, Canvas, filedialog, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk


THEME_COLOR = "#375362"
FONT_NAME = "Arial"


class Watermarker:
    def __init__(self):
        self.window = Tk()
        self.window.title("Watermarker")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Set window icon
        icon_path = "watermark-1.png"
        icon_img = Image.open(icon_path)
        self.window.iconphoto(True, ImageTk.PhotoImage(icon_img))

        label = Label(text="Watermarker", font=(
            "Times New Roman", 24, "bold"), bg=THEME_COLOR)
        label.grid(row=0, column=0, columnspan=2)

        open_button = Button(text="Open", command=self.open_file_dialog)
        open_button.grid(row=0, column=0, sticky="w")

        self.canvas: Canvas = Canvas(self.window, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.window.mainloop()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        self.image = Image.open(file_path)
        watermark_text = "WATERMARK"
        opacity = 0.1
        angle = 40
        watermark_image = self.add_watermark(
            self.image, watermark_text, opacity, angle)
        self.photo = ImageTk.PhotoImage(watermark_image)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        # reset geometry, so the window fits the new image
        # even after manual resize
        self.window.geometry(f"{self.image.width}x{self.image.height}")

    def add_watermark(self, image, text, opacity, angle):
        watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.load_default(size=image.width//8)

        draw.text((0, 0), text, font=font, fill=(
            255, 255, 255, int(255 * opacity)))
        rot_watermark = watermark.rotate(angle, expand=True)
        resized_watermark = rot_watermark.resize(image.size)

        return Image.alpha_composite(image.convert("RGBA"), resized_watermark)


if __name__ == "__main__":
    wm = Watermarker()
