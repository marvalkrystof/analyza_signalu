from PIL import Image
import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt

# načteme obrázek a převedeme ho na matici
image = Image.open("brain-mri.jpg") # převod na odstíny šedi
matrix = np.array(image)

# rozměry matice
print(matrix.shape)

# konvoluční jádro pro rozmazání
kernel_rozmazani = np.ones((3, 3)) / 9

# konvoluční jádro pro zostření
kernel_zostreni = np.array([[0, -1, 0], 
                            [-1, 5, -1], 
                            [0, -1, 0]])


# Uděláme kernely trojrozměrnými (obrázek je 2D + 1 rgb kanál = 3D)
kernel_3d_rozmazani = kernel_rozmazani[:, :, np.newaxis]
kernel_3d_zostreni = kernel_zostreni[:, :, np.newaxis]

# mode = "same" znamená, že výstupní matice bude mít stejný rozměr jako vstupní matice
result_rozmazani = convolve(
    matrix.astype(float),
    kernel_3d_rozmazani,
    mode="same",
)

# astype(float) je důležité, protože u této onvoluce může vést k záporným hodnotám nebo hodnotám větším než 255, což by mohlo způsobit chyby při převodu zpět na uint8.
# clip výstupní hodnoty do rozsahu 0-255, aby nedošlo k přetečení hodnot při konverzi zpět na uint8 (pokud jsem to neudělal, tak obrázek byl plný artefaktů)
result_zostreni = np.clip(convolve(
    matrix.astype(float),
    kernel_3d_zostreni,
    mode="same",
), 0, 255)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))


axes[0].imshow(image)
axes[0].set_title("Originál")
axes[0].axis("off")

axes[1].imshow(result_rozmazani.astype(np.uint8))
axes[1].set_title("Rozmazání")
axes[1].axis("off")

axes[2].imshow(result_zostreni.astype(np.uint8))
axes[2].set_title("Zostření")
axes[2].axis("off")

plt.tight_layout()
plt.show()
