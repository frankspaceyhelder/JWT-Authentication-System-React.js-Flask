const getState = ({ getStore, getActions, setStore }) => {
	return {
	  store: {
		token: localStorage.getItem("token") || null,
	  },
	  actions: {
		addToken: (inputToken) => {
		  localStorage.setItem("token", inputToken);
		  setStore({ token: inputToken });
		},
		removeToken: () => {
		  localStorage.removeItem("token");
		  setStore({ token: null });
		},
	  },
	};
  };
  
  export default getState;
  