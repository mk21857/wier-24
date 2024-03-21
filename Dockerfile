# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set environment name
ENV ENV_NAME wier

# Create and activate environment
RUN conda create -n $ENV_NAME python=3.9
RUN echo "source activate $ENV_NAME" >> ~/.bashrc
ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

# Install dependencies
RUN conda install -n $ENV_NAME selenium nb_conda requests -y
RUN conda install -n $ENV_NAME -c anaconda flask pyopenssl -y
RUN conda install -n $ENV_NAME -c conda-forge flask-httpauth -y
RUN /opt/conda/envs/$ENV_NAME/bin/pip install psycopg2-binary

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Command to run Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]