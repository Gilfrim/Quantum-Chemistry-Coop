import numpy as np
import os
from quant_rotor.models.dense.support_ham import write_matrix_elements, basis_m_to_p_matrix_conversion, H_kinetic, H_potential, H_kinetic_sparse, H_potential_sparse, H_potential_general
from scipy.sparse import diags, lil_matrix

np.set_printoptions(suppress = True, linewidth = 1500, threshold = 10000, precision = 9)

def hamiltonian(state: int, site: int, g_val: float, l_val: float=0, K_import: np.ndarray=[], V_import: np.ndarray=[], Import: bool=False, spar: bool=False, general: bool=False)->np.ndarray:
    """_summary_

    Parameters
    ----------
    state : int
        state of the system that 
    site : int
        _description_
    g_val : float
        _description_
    l_val : float, optional
        _description_, by default 0
    K_import : np.ndarray, optional
        _description_, by default []
    V_import : np.ndarray, optional
        _description_, by default []
    Import : bool, optional
        _description_, by default False

    Returns
    -------
    np.ndarray
        _description_
    """
    if Import == False:
        K, V = write_matrix_elements((state-1) // 2)

        # L_sparce = diags([l_val * 1/np.sqrt(2), 0, l_val * 1/np.sqrt(2)], offsets=[-1, 0, 1], shape=(state, state))

        # L_dense = L_sparce.toarray()

        # K = K + L_dense

        V_from_npy = V + V.T - np.diag(np.diag(V))
        V_tensor = V_from_npy.reshape(state, state, state, state)

        K_in_p = basis_m_to_p_matrix_conversion(K)
        V_in_p = basis_m_to_p_matrix_conversion(V_tensor)

        V_in_p = V_in_p.reshape(state**2, state**2)

    else:
        K_in_p = K_import
        V_in_p = V_import

    if spar:
        K_in_p = lil_matrix(K_in_p)
        V_in_p = lil_matrix(V_in_p)
        K_final = H_kinetic_sparse(state, site, K_in_p)
        V_final = H_potential_sparse(state, site, V_in_p, g_val)
    elif general:
        K_in_p = lil_matrix(K_in_p)
        V_in_p = lil_matrix(V_in_p)
        K_final = H_kinetic(state, site, K_in_p)
        V_final = H_potential_general(state, site, V_in_p, g_val)
    else:
        K_final = H_kinetic(state, site, K_in_p)
        V_final = H_potential(state, site, V_in_p, g_val)

    H_final = K_final + V_final

    return H_final, K_in_p, V_in_p

if __name__ == "__main__":
    site = 3
    state = 3
    print(hamiltonian(state, site))