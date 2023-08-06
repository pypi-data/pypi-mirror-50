from setuptools import setup


setup(
    name='FCMADRL',
    version='0.5dev',
    packages=['', 'FCMADRL/dqn', 'FCMADRL/ddpg'],
    install_requires=['tensorflow', 'keras', 'gym' ], 
    #dependenvy_links=['git+ssh://git@github.com/openai/multiagent-particle-envs.git#egg=multiagent-particle-envs'],
    url='https://github.com/Nikunj-Gupta/FCMADRL',
    license='MIT License',
    author='Nikunj Gupta',
    author_email='Nikunj.Gupta@iiitb.org',
    description='Fully Cooperative Multi-Agent Deep Reinforcement Learning'
)