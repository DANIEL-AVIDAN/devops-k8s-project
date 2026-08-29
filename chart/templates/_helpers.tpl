{{/* This is a comment - Generate basic labels */}}
{{- define "myapp.labels" }}
generator: helm
date: {{ now | htmlDate }}
app: {{ .Release.Name }}
{{- end }}

