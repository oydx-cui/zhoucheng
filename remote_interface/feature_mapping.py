# -*- coding: utf-8 -*-
import torch
import einops


class TensorSolution:

    def __init__(self, a, b, load):
        try:
            if a.shape[2] != 4 or b.shape[0] != 4:
                raise ValueError(
                    "The third dimension of tensor A and B must be 4.")
            if a.shape[3] != 2 or b.shape[1] != 2:
                raise ValueError(
                    "The fourth dimension of tensor A and B must be 2.")
            if a.shape[4] != 100 or b.shape[2] != 100:
                raise ValueError(
                    "The fifth dimension of tensor A and B must be 100.")

            # Tensor A and B
            self.TA = a
            self.TB = b
            self.load = load

        except ValueError as e:
            print(e)
            self.TA = None
            self.TB = None
            self.load = None

    def ORM(self):
        if self.TA is None or self.TB is None:
            print("Tensor A or Tensor B is not properly initialized.")
            return None

        try:
            if self.load < 0:
                raise ValueError("Load is less than 0")
            o1_size = 4
            # Integration
            TAh = einops.rearrange(self.TA[:, :, self.load, :, :],
                                   'o1 o2 o4 o5 -> (o1 o2) o4 o5')
            # Multi-Order Production
            Ah = torch.einsum('acd,bcd->ab', TAh, TAh)
            Bh = torch.einsum('abc,bc->a', TAh, self.TB[self.load, :, :])
            Ahinv = torch.linalg.pinv(Ah)
            x = torch.einsum('ba,a->b', Ahinv, Bh)
            TX = einops.rearrange(x, '(o1 o2) -> o1 o2', o1=o1_size)
            return TX

        except einops.EinopsError as e:
            print("Error during einops operation:", e)
            return None

        except IndexError as e:
            print("Index error occurred:", e)
            return None

        except TypeError as e:
            print("Dimension not matched error occurred:", e)
            return None

        except ValueError as e:
            print(e)
            return None

        except Exception as e:
            print("An unexpected error occurred:", e)
            return None
