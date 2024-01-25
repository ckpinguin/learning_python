from tkinter import Tk, Label, Button, Entry


window = Tk()

window.title("Mile to Km Converter")
# window.minsize(width=600, height=480)
window.config(padx=20, pady=20)

miles_entry = Entry(width=10)
miles_entry.grid(row=1, column=2)

miles_label = Label(text="Miles")
miles_label.grid(row=1, column=3)

is_equal_label = Label(text="is equal to")
is_equal_label.grid(row=2, column=1)

km_result_label = Label(text=0)
km_result_label.grid(row=2, column=2)

km_label = Label(text="Km")
km_label.grid(row=2, column=3)


def calculate_km():
    km = float(miles_entry.get()) * 1.609344
    km_result_label.config(text=f"{km:.4f}")


button_calc = Button(text="Calculate", command=calculate_km)
button_calc.grid(row=3, column=2)


window.mainloop()
