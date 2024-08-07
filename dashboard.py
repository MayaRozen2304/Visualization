import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
import zipfile
import sys

plt.switch_backend('Agg')

def main():
    zip_file_path = 'okcupid_profiles.zip'
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('extracted_folder')  # Extract to a folder named 'extracted_folder'
    csv_file_path = 'extracted_folder/okcupid_profiles.csv'
    data = pd.read_csv(csv_file_path)
    
    # data = pd.read_csv("okcupid_profiles.csv")
    st.title('Data Visualization Final Project - OkCupid Users Insights Dashboard')

    # Sidebar
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Go to", ["Categorical Variables Distributions", "Age Distribution", "User Intents", "User Activity Trends"])

    # Define the first tab content
    if tab == "Categorical Variables Distributions":
        # Select the categorical column
        categorical_columns = ['orientation', 'status','drinks', 'drugs', 'smokes']
        selected_column = st.selectbox('Select a Categorical Column', categorical_columns)

        # Set the dynamic title for tab 1
        st.header(f'Distribution of {selected_column.capitalize()}')

        # Group data by the selected column and sex
        grouped_data = data.groupby([selected_column, 'sex']).size().unstack(fill_value=0)
        total_users = grouped_data.sum(axis=1)

        if 'm' in grouped_data.columns and 'f' in grouped_data.columns:
            percent_m = (grouped_data['m'] / total_users) * 100
            percent_f = (grouped_data['f'] / total_users) * 100

            plt.figure(figsize=(20, 12))

            # Get the categories as x-axis labels
            categories = grouped_data.index
            x = range(len(categories))

            bar_width = 0.35

            plt.bar(x, grouped_data['m'], width=bar_width, color='skyblue', align='center', label='Male')
            plt.bar([i + bar_width for i in x], grouped_data['f'], width=bar_width, color='lightcoral', align='center',
                    label='Female')

            for i, category in enumerate(categories):
                plt.text(i, grouped_data.loc[category, 'm'] + 1,
                         f"{percent_m.loc[category]:.1f}%", ha='center', va='bottom',fontsize=20)
                plt.text(i + bar_width, grouped_data.loc[category, 'f'] + 1,
                         f"{percent_f.loc[category]:.1f}%", ha='center', va='bottom',fontsize=20)


            # for i, category in enumerate(categories):
            #     plt.text(i, grouped_data.loc[category, 'm'] + 1,
            #              f"{grouped_data.loc[category, 'm']} ({percent_m.loc[category]:.1f}%)", ha='center', va='bottom',fontsize=20)
            #     plt.text(i + bar_width, grouped_data.loc[category, 'f'] + 1,
            #              f"{grouped_data.loc[category, 'f']} ({percent_f.loc[category]:.1f}%)", ha='center', va='bottom',fontsize=20)

            plt.title(f'{selected_column.capitalize()} Distribution by Gender among OkCupid Users',fontsize=35)
            plt.xlabel(selected_column.capitalize(), fontsize=25)
            plt.ylabel('Number of Users', fontsize=25)
            plt.xticks([i + bar_width / 2 for i in x], categories, rotation=45,fontsize=25)
            plt.yticks(fontsize=25)
            plt.legend(fontsize=25)
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write(f"No data available for the selected column: {selected_column}")

    # Define the second tab content
    elif tab == "Age Distribution":
        data['age'] = data['age'].fillna(data['age'].mean())
        sns.set_style("white")
        xlims = [(15, 70)]
        titles = ['Age Distribution']

        # Create subplot for age distribution
        fig, ax = plt.subplots(ncols=1, figsize=(8, 6))

        sns.histplot(data=data, x='age', ax=ax, hue='sex', element='step', bins=40, alpha=0.4)
        ax.set(xlim=xlims[0], title=titles[0])
        plt.tight_layout()
        st.pyplot(fig)

    elif tab == "User Intents":

        # Aggregate essays into a single profile string
        data["Profile"] = data[["essay0", "essay1", "essay2", "essay3", "essay4",
                                "essay5", "essay6", "essay7", "essay8", "essay9"]].astype(str).agg(' '.join, axis=1)
        text = ' '.join(data["Profile"].astype(str))
    
        # Streamlit inputs
        specific_words_input = st.text_input(
            "Enter specific words separated by commas (e.g., kind, funny, intelligent):",
            "kind, funny, intelligent, casual, hook, love, fun, adventurous, ambitious, honest, loyal"
        )
        specific_words = [word.strip() for word in specific_words_input.split(',')]
    
        max_words = st.slider("Max number of words in word cloud:", min_value=1, max_value=50, value=11)
    
        # Calculate word frequencies
        word_freq = {word: text.count(word) for word in specific_words}
    
        # Generate word cloud
        wordcloud = WordCloud(max_words=max_words, background_color="white").generate_from_frequencies(word_freq)
    
        # Display word cloud
        plt.figure(figsize=(8, 5))
        plt.title('Word Frequency in User Descriptions', pad=20)  # Adjust 'pad' for title spacing
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(plt)


    
        # data["Profile"] = data[["essay0", "essay1", "essay2", "essay3", "essay4",
        #                         "essay5", "essay6", "essay7", "essay8", "essay9"]].astype(str).agg(' '.join, axis=1)
        # text = ' '.join(data["Profile"].astype(str))

        # specific_words = ["kind", "funny", "intelligent", "casual", "hook", "love",
        #                   "fun", "adventurous", "ambitious", "honest", "loyal"]

        # word_freq = {word: text.count(word) for word in specific_words}
        # wordcloud = WordCloud(max_words=11, background_color="white").generate_from_frequencies(word_freq)

        # plt.figure(figsize=(8, 5))
        # plt.title('Word Frequency in User Descriptions', pad=20)  # Adjust 'pad' for title spacing
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # plt.tight_layout()
        # st.pyplot(plt)

    # elif tab == "User Intents":

    #     data["Profile"] = data[["essay0", "essay1", "essay2", "essay3", "essay4",
    #                         "essay5", "essay6", "essay7", "essay8", "essay9"]].astype(str).agg(' '.join, axis=1)
    #     text = ' '.join(data["Profile"].astype(str))

    #     specific_words = ["kind", "funny", "intelligent", "casual", "hook", "love",
    #                   "fun", "adventurous", "ambitious", "honest", "loyal"]
    
    #     word_freq = {word: text.count(word) for word in specific_words}
    #     wordcloud = WordCloud(max_words=11, background_color="white").generate_from_frequencies(word_freq)
    
    #     plt.figure(figsize=(8, 5))
    #     plt.title('Word Frequency in User Descriptions', pad=20)  # Adjust 'pad' for title spacing
    #     plt.imshow(wordcloud, interpolation='bilinear')
    #     plt.axis("off")
    
    #     # Add word frequencies
    #     for word, freq in word_freq.items():
    #         # Find the position of the word in the word cloud
    #         positions = wordcloud.layout_
    #         for (word_position, word_freq, font_size, position, orientation, color) in positions:
    #             if word == word_position:
    #                 plt.text(position[0], position[1], f'{word} ({freq})', fontsize=font_size, color=color, ha='center', va='center')
    
    #     plt.tight_layout()
    #     st.pyplot(plt)

    elif tab == "User Activity Trends":
        st.header('User Activity Trends')

        # Move the dropdown into the main plot area
        color_by = st.selectbox('Select a Categorical Column', ['orientation', 'sex'])

        data['hour'] = data['last_online'].apply(lambda x: '0' if x.split('-')[3] == '00' else x.split('-')[3])
        data['hour'] = pd.to_numeric(data['hour'])

        hourly_counts = data.groupby(['hour', color_by]).size().unstack(fill_value=0)

        plt.figure(figsize=(20, 15))

        for category in hourly_counts.columns:
            plt.plot(hourly_counts.index, hourly_counts[category], marker='o', linestyle='-', linewidth=2,
                     label=category)

        plt.title('Number of Users by Hour of Last Online',fontsize=35)
        plt.xlabel('Hour of Last Online',fontsize=25)
        plt.ylabel('Number of Users',fontsize=25)
        plt.xticks(hourly_counts.index,
                   [f'{hour:02}' if hour in range(0, 10) else f'{hour}' for hour in hourly_counts.index], fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(title=color_by.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left',fontsize=25,title_fontsize=25)
        plt.tight_layout()
        st.pyplot(plt)


if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
