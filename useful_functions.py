def model_results_new(data, data_type, model, X_train_num, X_test_num, y_train, y_test):
    
    master_dict = {
    'Data_Used': [],
    'Data_Type': [],
    'Model_Name': [],
    'Model_Training_Score' : [],
    'Model_Test_Score': [],
    'Mean_Squared_Error': [],
    'Model_Cross_Val_Score': [],
    'Coefficients/Feature_Importances': [],
    'Grid_Search_Best_Params / Regularization_Params': [],
    'Notes': []
}  
    
    #Update The Data Column With The Type of Data (Numeric vs Text vs All)
    
    if data == 1:
        master_dict['Data_Used'].append('Text + Numerical Data')
    else:
        master_dict['Data_Used'].append('Numerical')
    
    
    #Updating With The Type of Data
        
    if data_type == 'logged':
        master_dict['Data_Type'].append('Logged')
    else:
        master_dict['Data_Type'].append('Non-Logged Data')
        
    
    #Extracting Out All Of The Relevant Information
    
    fitted_model = model.fit(X_train_num, y_train)
    master_dict['Model_Name'].append(str(fitted_model))
    master_dict['Model_Training_Score'].append(fitted_model.score(X_train_num, y_train))
    master_dict['Model_Test_Score'].append(fitted_model.score(X_test_num, y_test))
    predictions = fitted_model.predict(X_test_num) 
    master_dict['Mean_Squared_Error'].append(mean_squared_error(y_test, predictions))
    master_dict['Model_Cross_Val_Score'].append(np.mean(cross_val_score(fitted_model, X_train_num, y_train, cv=5)))

    try:
        master_dict['Coefficients/Feature_Importances'].append(dict(coefficient_values = fitted_model.coef_, 
                                       indexes = X_train_num.columns))
    except:
        master_dict['Coefficients/Feature_Importances'].append(dict(coefficient_values = fitted_model.feature_importances_, 
                                       indexes = X_train_num.columns))
                      
            
    try:
        master_dict['Grid_Search_Best_Params / Regularization_Params'].append(fitted_model.best_params_)
    except:
        try:
            master_dict['Grid_Search_Best_Params / Regularization_Params'].append(fitted_model.alpha_)
        except:
            master_dict['Grid_Search_Best_Params / Regularization_Params'].append('No Grid Search Used')
    
            
    master_dict['Notes'].append(str(fitted_model))
     
    df = pd.DataFrame(master_dict)
    return df





def plot_y_yhat(y, yhat):

    fig = plt.figure(figsize=(7,7))
    ax = fig.gca()

    ax.scatter(y, yhat, color='darkgoldenrod', s=70, label='yhat - true y')

    max_val = np.max(y)
    min_val = np.min(y)

    ax.plot([min_val, max_val], [min_val, max_val], color='darkgreen',
            linewidth=4.0, alpha=0.7, label='perfect model')

    ax.set_xlabel('true y', fontsize=16)
    ax.set_ylabel('yhat', fontsize=16)

    plt.legend(loc='upper left')

    plt.show()
    
plot_y_yhat(height, wr_height_hat)