{{/* This is a comment - Generate basic labels */}}
{{- define "myapp.labels" }}
generator: helm
app: {{ .Release.Name }}
{{- end }}

